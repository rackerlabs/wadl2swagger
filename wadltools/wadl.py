from wadllib.application import Application, Resource, WADLError
from lxml import etree
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
    def short_desc(wadl_object):
        # HACK: OpenStack specific...
        return DocHelper.doc_tag(wadl_object).find('./{' + WADL.NAMESPACES['docbook'] + "}para[@role='shortdesc']")

    @staticmethod
    def convert_description(doc_tag, description=''):
        elem = DocHelper.element_for(doc_tag)
        elem.text = doc_tag.text
        for tag in list(doc_tag):
            elem.append(DocHelper.convert_description(tag))
        elem.tail = doc_tag.tail

        return elem

    @staticmethod
    def description_text(doc_tag):
        return etree.tostring(etree.ElementTree(DocHelper.convert_description(doc_tag)))

    @staticmethod
    def element_for(doc_tag):
        tag_type = doc_tag.tag
        attrs = {}
        if tag_type == WADL.qname('docbook', 'citetitle'):
            tag = "p"
        elif tag_type == WADL.qname('docbook', 'code'):
            tag = "code"
        elif tag_type == WADL.qname('docbook', 'emphasis'):
            tag = "strong"
        elif tag_type == WADL.qname('docbook', 'link'):
            tag = "a"
            attrs['href'] = doc_tag.get(WADL.qname('xlink', 'href'))
        elif tag_type == WADL.qname('docbook', 'listitem'):
            tag = "li"
        elif tag_type == WADL.qname('docbook', 'literal'):
            tag = "p"
        elif tag_type == WADL.qname('docbook', 'note'):
            tag = "p"
        elif tag_type == WADL.qname('docbook', 'olink'):
            tag = "p"
        elif tag_type == WADL.qname('docbook', 'para'):
            tag = "p"
        elif tag_type == WADL.qname('docbook', 'parameter'):
            tag = "p"
        elif tag_type == WADL.qname('docbook', 'term'):
            tag = "p"
        elif tag_type == WADL.qname('docbook', 'variablelist'):
            tag = "p"
        elif tag_type == WADL.qname('docbook', 'varlistentry'):
            tag = "p"
        elif tag_type == WADL.qname('docbook', 'warning'):
            tag = "p"
        elif tag_type == WADL.qname('wadl', 'doc'):
            tag = "p"
        elif tag_type == WADL.qname('docbook', 'replaceable'):
            # FIXME: What should this be?
            tag = "em"
        elif tag_type == WADL.qname('docbook', 'itemizedlist'):
            tag = "ul"
        elif tag_type == WADL.qname('docbook', 'strong'):
            tag = "strong"
        elif tag_type == WADL.qname('docbook', 'xref'):
            logging.warning("xref is not properly supported")
            tag = "cite"
        elif tag_type.startswith(WADL.qname('xhtml')):
            tag = tag_type.replace(WADL.qname('xhtml'), '')
        else:
            raise ValueError("Unknown doc tag type: %s" % tag_type)
        e = etree.Element(tag)
        for key, value in attrs.iteritems():
            if value is not None:
                e.set(key, value)
        return e
