import os
import sys
import urlparse, urllib
from wadllib.application import Application, Resource
import yaml

def path2url(path):
    return urlparse.urljoin(
      'file:', urllib.pathname2url(path))

# Hack around https://bugs.launchpad.net/wadllib/+bug/1273846
def hack_namespace(wadl_string):
    return wadl_string.replace(
      "http://wadl.dev.java.net/2009/02",
      "http://research.sun.com/wadl/2006/10"
    )

def application_for(filename):
    url = path2url(filename)
    wadl_string = open(filename, 'r').read()
    return Application(url, hack_namespace(wadl_string))

def save_swagger(swagger, filename):
    with open(filename, 'w') as yaml_file:
      yaml_file.write( yaml.dump(swagger, default_flow_style=False) )

class SwaggerBuilder:
    def xsd_to_json_type(self, xsd_type):
        # This should probably be more namespace aware (e.g. handle xs:string or xsd:string)
        try:
          return {
            # array?
            "xsd:boolean": "boolean", # is xsd:bool also valid?
            "xsd:integer": "integer",
            "xsd:decimal": "number",
            # null?
            # object/complex types?
            "xsd:string": "string",
            "xsd:date": "string", # should be string w/ format or regex
            "xsd:time": "string"  # should be string w/ format or regex
          }[xsd_type]
        except KeyError:
          print "WARN: Using unknown type: %s" % xsd_type
          return xsd_type

    def style_to_in(self, style):
        return {
          "matrix": "unknown",
          "query": "query",
          "header": "header",
          "template": "path",
          "plain": "path"
        }[style]

    def build_param(self, wadl_param):
        print "Found param: %s" % wadl_param.name

        return {
          "name": wadl_param.name,
          "required": wadl_param.is_required,
          "in": self.style_to_in(wadl_param.style),
          "type": self.xsd_to_json_type(wadl_param.tag.attrib['type'])
        }


wadl_file = os.path.realpath("wadls/identity-admin.wadl")
swagger_file = os.path.realpath("swagger/identity-admin.yaml")
wadl = application_for(wadl_file)
swagger_builder = SwaggerBuilder()
print "Reading WADL from %s" % wadl_file
swagger = {
  "swagger": 2,
  "info": {
    "contact": {
      "name": "Rackspace"
    },
    "description": "Placeholder",
    "license": {
      "name": "Placeholder",
      "url": "Placeholder"
    },
    "termsOfService": "Placeholder",
    "title": "Placeholder",
    "version": "Placeholder"
  },
  "paths": {}
}

for resource_element in wadl.resources:
  path = resource_element.attrib['path']
  resource = wadl.get_resource_by_path(path)
  swagger_resource = swagger["paths"][path] = {}
  print "  Processing resource for %s" % path
  swagger_resource["parameters"] = []

  # Resource level parameters
  try:
    # for param_name in resource.parameter_names('application/json'):
    for param in resource.params('application/json'):
      swagger_resource["parameters"].append(swagger_builder.build_param(param))
  except AttributeError:
    print "   WARN: wadllib can't get parameters, possibly a wadllib bug"
    print "     (It seems like it only works if the resource has a GET method"

  for method in resource.method_iter:
    print "    Processing method %s %s" % (method.name, path)
    swagger_method = swagger_resource[method.name] = {}
    swagger_method['consumes'] = []
    swagger_method['produces'] = []
    swagger_method['parameters'] = []
    if method.request.tag is not None:
      request = method.request
      for representation in request.representations:
        print "Class: %s" % representation.__class__.__name__
        swagger_method['consumes'].append(representation.media_type)
        for param in representation.params(resource):
          swagger_resource["parameters"].append(swagger_builder.build_param(param))

    if method.response.tag is not None:
      response = method.response
      # Not properly iterable - plus we're focused on json
      # for representation in response.representation:
      representation = response.get_representation_definition('application/json')
      if representation is not None:
        swagger_method['produces'].append(representation.media_type)

print "Saving swagger to %s" % swagger_file
save_swagger(swagger, swagger_file)
