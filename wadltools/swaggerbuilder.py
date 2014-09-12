import yaml
import textwrap
from collections import OrderedDict
from wadltools.wadl import DocHelper

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
        param = OrderedDict()
        param['name'] = wadl_param.name
        param['required'] = wadl_param.is_required
        param['in'] = self.style_to_in(wadl_param.style)

        if type is not None:
            param["type"] = type
        if DocHelper.doc_tag(wadl_param) is not None and DocHelper.doc_tag(wadl_param).text is not None:
            description = DocHelper.description_text(DocHelper.doc_tag(wadl_param))
            # Cleanup whitespace...
            description = textwrap.dedent(description)
            param["description"] = folded(description)
        return param

    def build_response(self, wadl_response):
        status = wadl_response.tag.attrib['status']
        try:
            description = ' '.join(
                DocHelper.doc_tag(wadl_response).text.split())
        except:
            description = "%s response" % status

        return {
            "description": literal(description)
        }

    def build_code_sample(self, wadl_code_sample):
        examples = OrderedDict()
        examples['application/json'] = literal(wadl_code_sample.text)
        return examples

# pyyaml presenters

class quoted(str): pass

def quoted_presenter(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')
yaml.add_representer(quoted, quoted_presenter)

class folded(unicode): pass

def folded_presenter(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='>')
yaml.add_representer(folded, folded_presenter)

class literal(unicode): pass

def literal_presenter(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
yaml.add_representer(literal, literal_presenter)

def ordered_dict_presenter(dumper, data):
    return dumper.represent_dict(data.items())
yaml.add_representer(OrderedDict, ordered_dict_presenter)
