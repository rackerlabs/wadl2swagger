#!/bin/bash
set -e

python setup.py install
./bin/wadlcrawler http://api.rackspace.com/wadls/
# The cloud_monitoring WADL has a few issues, its a WIP
rm wadls/cloud_monitoring.wadl
./bin/wadl2swagger --autofix wadls/*.wadl

