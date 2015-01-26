import pypandoc
from wadllib.application import Application, Resource, WADLError
from lxml import etree
# etree & ElementTree :(
try:
    import xml.etree.cElementTree as ET
except ImportError:
    try:
        import cElementTree as ET
    except ImportError:
        import elementtree.ElementTree as ET
import urlparse
import urllib
import logging


class BadWADLError(Exception):

    def __init__(self, message, base_exception, wadl_file):

        full_msg = "%s, caused by \"%s: %s\" while loading %s" % (
            message, type(base_exception).__name__, base_exception.message, wadl_file)
        # Call the base class constructor with the parameters it needs
        super(BadWADLError, self).__init__(full_msg)


class WADL:

    WADL_NAMESPACE = "http://wadl.dev.java.net/2009/02"
    LEGACY_WADL_NAMESPACE = "http://research.sun.com/wadl/2006/10"

    NAMESPACES = {
        "docbook": "http://docbook.org/ns/docbook",
        "xlink": "http://www.w3.org/1999/xlink",
        "wadl": LEGACY_WADL_NAMESPACE,
        "xsdxt": "http://docs.rackspacecloud.com/xsd-ext/v1.0",
        "xhtml": "http://www.w3.org/1999/xhtml"
    }

    @staticmethod
    def qname(prefix, tag=''):
        return "{" + WADL.NAMESPACES[prefix] + "}" + tag

    @staticmethod
    def application_for(filename):
        def path2url(path):
            return urlparse.urljoin(
                'file:', urllib.pathname2url(path))

        def hack_namespace(wadl_string):
            return wadl_string.replace(
                WADL.WADL_NAMESPACE,
                WADL.LEGACY_WADL_NAMESPACE
            )

        url = path2url(filename)
        wadl_string = open(filename, 'r').read()
        try:
            return Application(url, hack_namespace(wadl_string))
        # except (WADLError, ParseError) as e:
        except Exception as e:
            raise BadWADLError("Could not load WADL file", e, url)


class DocHelper:

    @staticmethod
    def wadl_tag(wadl_object, tag_name):
        return wadl_object.tag.find('./{' + WADL.LEGACY_WADL_NAMESPACE + '}' + tag_name)

    @staticmethod
    def doc_tag(wadl_object):
        return DocHelper.wadl_tag(wadl_object, 'doc')

    @staticmethod
    def short_desc_as_markdown(wadl_object):
        short_desc = DocHelper.doc_tag(wadl_object).find('./{' + WADL.NAMESPACES['docbook'] + "}para[@role='shortdesc']")
        return DocHelper.docbook_to_markdown(short_desc)

    @staticmethod
    def docbook_to_markdown(doc_tag):
        # We need to convert the element to an XML string
        # And tostring doesn't like the namespaces for some reason...
        for prefix, namespace in doc_tag.attrib['xmlns:map'].iteritems():
            ET.register_namespace(prefix, namespace)
        if 'xmlns:map' in doc_tag.attrib:
            del doc_tag.attrib['xmlns:map']
        for e in doc_tag.iter():
            if 'xmlns:map' in e.attrib:
                del e.attrib['xmlns:map']
        doc_tag_source = ET.tostring(doc_tag)
        markdown = pypandoc.convert(doc_tag_source, 'markdown_github', format="docbook")
        return pypandoc.convert(doc_tag_source, 'markdown_github', format="docbook")
