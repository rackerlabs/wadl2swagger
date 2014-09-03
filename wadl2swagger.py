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

wadl_file = os.path.realpath("wadls/identity-admin.wadl")
swagger_file = os.path.realpath("swagger/identity-admin.yaml")
wadl = application_for(wadl_file)
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
  for method in resource.method_iter:
    print "    Processing method %s" % method.name
    swagger_method = swagger_resource[method.name] = {}
    swagger_method['consumes'] = []
    swagger_method['produces'] = []
    if method.request.tag is not None:
      request = method.request
      for representation in request.representations:
        swagger_method['consumes'].append(representation.media_type)
    if method.response.tag is not None:
      response = method.response
      # Not properly iterable - plus we're focused on json
      # for representation in response.representation:
      representation = response.get_representation_definition('application/json')
      if representation is not None:
        swagger_method['produces'].append(representation.media_type)

print "Saving swagger to %s" % swagger_file
save_swagger(swagger, swagger_file)
