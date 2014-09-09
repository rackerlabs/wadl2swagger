import os
import sys
import urlparse
import urllib
from wadllib.application import Application, Resource
import yaml
from xml.etree import ElementTree
from xml.etree.ElementTree import Element


def path2url(path):
    return urlparse.urljoin(
        'file:', urllib.pathname2url(path))

WADL_NAMESPACE = "http://wadl.dev.java.net/2009/02"
LEGACY_WADL_NAMESPACE = "http://research.sun.com/wadl/2006/10"

# Hack around https://bugs.launchpad.net/wadllib/+bug/1273846


def hack_namespace(wadl_string):
    return wadl_string.replace(
        WADL_NAMESPACE,
        LEGACY_WADL_NAMESPACE
    )


def application_for(filename):
    url = path2url(filename)
    wadl_string = open(filename, 'r').read()
    return Application(url, hack_namespace(wadl_string))


def save_swagger(swagger, filename):
    with open(filename, 'w') as yaml_file:
        yaml_file.write(yaml.dump(swagger, default_flow_style=False))


class DocHelper:

    @staticmethod
    def wadl_tag(wadl_object, tag_name):
        return wadl_object.tag.find('./{' + LEGACY_WADL_NAMESPACE + '}' + tag_name)

    @staticmethod
    def doc_tag(wadl_object):
        return DocHelper.wadl_tag(wadl_object, 'doc')

    @staticmethod
    def convert_description(doc_tag, description=''):
        elem = DocHelper.element_for(doc_tag)
        elem.text = doc_tag.text
        for tag in list(doc_tag):
            elem.append(DocHelper.convert_description(tag))
        elem.tail = doc_tag.tail

        return elem

    @staticmethod
    def element_for(doc_tag):
        tag_type = doc_tag.tag
        attrs = {}
        if tag_type == "{http://docbook.org/ns/docbook}citetitle":
            tag = "p"
        elif tag_type == "{http://docbook.org/ns/docbook}code":
            tag = "code"
        elif tag_type == "{http://docbook.org/ns/docbook}emphasis":
            tag = "strong"
        elif tag_type == "{http://docbook.org/ns/docbook}link":
            tag = "a"
            attrs['href'] = doc_tag.get('{http://www.w3.org/1999/xlink}href')
        elif tag_type == "{http://docbook.org/ns/docbook}listitem":
            tag = "li"
        elif tag_type == "{http://docbook.org/ns/docbook}literal":
            tag = "p"
        elif tag_type == "{http://docbook.org/ns/docbook}note":
            tag = "p"
        elif tag_type == "{http://docbook.org/ns/docbook}olink":
            tag = "p"
        elif tag_type == "{http://docbook.org/ns/docbook}para":
            tag = "p"
        elif tag_type == "{http://docbook.org/ns/docbook}parameter":
            tag = "p"
        elif tag_type == "{http://docbook.org/ns/docbook}term":
            tag = "p"
        elif tag_type == "{http://docbook.org/ns/docbook}variablelist":
            tag = "p"
        elif tag_type == "{http://docbook.org/ns/docbook}varlistentry":
            tag = "p"
        elif tag_type == "{http://docbook.org/ns/docbook}warning":
            tag = "p"
        elif tag_type == "{http://research.sun.com/wadl/2006/10}doc":
            tag = "p"
        elif tag_type.startswith("{http://www.w3.org/1999/xhtml}"):
            tag = tag_type.replace('{http://www.w3.org/1999/xhtml}', '')
        else:
            print "Unknown doc tag type: %s" % ElementTree.QName(tag_type)
        e = Element(tag)
        for key, value in attrs.iteritems():
            if value is not None:
                e.set(key, value)
        return e


class SwaggerBuilder:

    def xsd_to_json_type(self, xsd_type):
        if xsd_type is None:
            return "string"
        # This should probably be more namespace aware (e.g. handle xs:string
        # or xsd:string)
        try:
            return {
                # array?
                "xsd:boolean": "boolean",  # is xsd:bool also valid?
                "xsd:integer": "integer",
                "xsd:decimal": "number",
                # null?
                # object/complex types?
                "xsd:string": "string",
                "xsd:date": "string",  # should be string w/ format or regex
                "xsd:time": "string"  # should be string w/ format or regex
            }[xsd_type]
        except KeyError:
            print "WARN: Using unknown type: %s" % xsd_type
            # return xsd_type
            return None

    def style_to_in(self, style):
        return {
            "matrix": "unknown",
            "query": "query",
            "header": "header",
            "template": "path",
            "plain": "body"
        }[style]

    def build_summary(self, documented_wadl_object):
        return DocHelper.doc_tag(documented_wadl_object).attrib['title']

    def build_param(self, wadl_param):
        print "Found param: %s" % wadl_param.name

        type = self.xsd_to_json_type(wadl_param.tag.get('type', 'string'))
        param = {
            "name": wadl_param.name,
            "required": wadl_param.is_required,
            "in": self.style_to_in(wadl_param.style),
        }
        if type is not None:
            param["type"] = type
        if DocHelper.doc_tag(wadl_param) is not None and DocHelper.doc_tag(wadl_param).text is not None:
            description_elem = DocHelper.convert_description(
                DocHelper.doc_tag(wadl_param))
            param["description"] = ElementTree.tostring(description_elem)
        return param

    def build_response(self, wadl_response):
        status = wadl_response.tag.attrib['status']
        try:
            description = ' '.join(
                DocHelper.doc_tag(wadl_response).text.split())
        except:
            description = "%s response" % status

        return {
            "description": description
        }


def convert_wadl(wadl_file, swagger_file):
    title = os.path.splitext(os.path.split(wadl_file)[1])[0]
    wadl = application_for(wadl_file)
    swagger_builder = SwaggerBuilder()
    print "Reading WADL from %s" % wadl_file
    swagger = {
        "swagger": 2,
        "info": {
            #   "contact": {
            #     "name": "Rackspace"
            #   },
            #   "description": "Placeholder",
            #   "license": {
            #     "name": "Placeholder",
            #     "url": "Placeholder"
            #   },
            #   "termsOfService": "Placeholder",
            "title": title,
            "version": "Unknown"
        },
        "paths": {},
        "consumes": [  # default consumes, maybe it shouldn't be hardcoded?
            "application/json"
        ]
    }

    for resource_element in wadl.resources:
        path = resource_element.attrib['path']
        resource = wadl.get_resource_by_path(path)
        swagger_resource = swagger["paths"][path] = {}
        print "  Processing resource for %s" % path

        # Resource level parameters
        try:
            for param in resource.params('application/json'):
                if "parameters" not in swagger_resource:
                    swagger_resource["parameters"] = []
                swagger_resource["parameters"].append(
                    swagger_builder.build_param(param))
        except AttributeError:
            print "   WARN: wadllib can't get parameters, possibly a wadllib bug"
            print "     (It seems like it only works if the resource has a GET method"

        for method in resource.method_iter:
            print "    Processing method %s %s" % (method.name, path)
            swagger_method = swagger_resource[method.name] = {}
            # Rackspace specific...
            if '{http://docs.rackspace.com/api}id' in method.tag.attrib:
                swagger_method['operationId'] = method.tag.attrib[
                    '{http://docs.rackspace.com/api}id']
            swagger_method['summary'] = swagger_builder.build_summary(method)
            # swagger_method['operationId'] = method.tag.attrib['id']
            # swagger_method['consumes'] = []
            swagger_method['produces'] = []
            swagger_method['responses'] = {}
            if method.request.tag is not None:
                request = method.request
                for representation in request.representations:
                    # Swagger schema needs to be updated to allow consumes here
                    # swagger_method['consumes'].append(representation.media_type)
                    for param in representation.params(resource):
                        if "parameters" not in swagger_method:
                            swagger_method['parameters'] = []
                        swagger_method["parameters"].append(
                            swagger_builder.build_param(param))

            if method.response.tag is not None:
                response = method.response
                # Not properly iterable - plus we're focused on json
                # for representation in response.representation:
                representation = response.get_representation_definition(
                    'application/json')
                if representation is not None:
                    swagger_method['produces'].append(
                        representation.media_type)
                for status in response.tag.attrib['status'].split():
                    swagger_method['responses'][
                        int(status)] = swagger_builder.build_response(response)

    print "Saving swagger to %s" % swagger_file
    save_swagger(swagger, swagger_file)

import fnmatch
import os

wadl_dir = 'wadls/'
swagger_dir = 'swagger/'

for root, dirs, files in os.walk(wadl_dir):
    for filename in fnmatch.filter(files, '*.wadl'):
        filename, extname = os.path.splitext(filename)
        wadl_file = os.path.join(wadl_dir, filename + extname)
        swagger_file = os.path.join(swagger_dir, filename + '.yaml')
        convert_wadl(wadl_file, swagger_file)
