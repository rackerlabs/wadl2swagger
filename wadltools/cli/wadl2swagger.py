# -*- coding: utf-8 -*-

import os, errno
import argparse
import logging

import wadltools
from wadltools import WADL, SwaggerConverter
from collections import OrderedDict
import yaml

def mkdir_p(path):
        try:
            os.makedirs(path)
        except OSError as exc: # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else: raise

def main():
    parser = argparse.ArgumentParser()

    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('--swagger-dir', type=str, default='swagger/', help='output folder for converted Swagger files')
    parser.add_argument('--merge-dir', type=str, default='defaults/', help='folder contains partial Swagger YAML files to merge with the WADL data')
    parser.add_argument('--autofix', dest='autofix', action='store_true', help='fix common Swagger issues (rather than fixing them by standardizing WADL)')
    parser.add_argument('wadl_file', nargs='+', metavar='WADL_FILE', help="wadl files to convert")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, filename='wadl2swagger.log', filemode='w')
    else:
        logging.basicConfig(level=logging.INFO, filename='wadl2swagger.log', filemode='w')
    logging.getLogger('').addHandler(logging.StreamHandler())

    for wadl_file in args.wadl_file:
        filename, wadl_ext = os.path.splitext(os.path.split(wadl_file)[1]) # better way to get basename w/out ext?
        swagger_file = os.path.join(args.swagger_dir, filename + '.yaml')
        mkdir_p(os.path.dirname(swagger_file))
        converter = SwaggerConverter(args)
        swagger = converter.convert(filename, wadl_file, swagger_file)
        logging.info("Saving swagger to %s", swagger_file)
        save_swagger(swagger, swagger_file)

def save_swagger(swagger, filename):
    with open(filename, 'w') as yaml_file:
        yaml_file.write(yaml.dump(swagger, default_flow_style=False))

if __name__ == '__main__':
    main()

