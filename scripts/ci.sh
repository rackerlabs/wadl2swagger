#!/bin/bash
set -e

if [ "$CI" = "true" ]; then
  # We're on Snap-CI, Travis, etc.
  python setup.py install
else
  python setup.py develop
fi

wadlcrawler http://api.rackspace.com/wadls/
# The cloud_monitoring WADL has a few issues, its a WIP
rm wadls/cloud_monitoring.wadl
wadl2swagger --autofix wadls/*.wadl

echo "Unknown types summary:"
cat wadl2swagger.log | grep 'Using unknown' | cut -d' ' -f2- | sort | uniq

echo
echo
echo "Warning Summary:"
cat wadl2swagger.log | grep 'WARNING:' | sort | uniq
