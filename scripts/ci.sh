#!/bin/bash
if [ "$CI" = "true" ]; then
  # We're on Snap-CI, Travis, etc.
  python setup.py install
else
  python setup.py develop
fi

function fail_unless_expected {
  echo $1
  if [[ "$1" == *"cloud_monitoring"* ]] || [[ "$1" == *"email"* ]] ; then
    echo $1 failed but is not expected to work
  else
    echo $1 failed
    exit 1
  fi
}

wadlcrawler http://api.rackspace.com/wadls/
for wadl in wadls/*.wadl; do
  basename=${wadl%.wadl}
  wadl2swagger --autofix $wadl -l "$basename.log"
  if [ $? -ne 0 ]; then
    fail_unless_expected $wadl
  fi
done
# rm wadls/cloud_monitoring.wadl # The cloud_monitoring WADL has a few issues, its a WIP
rm wadls/email*.wadl # Skip mailgun
wadl2swagger --autofix wadls/*.wadl

echo "Unknown types summary:"
cat wadl2swagger.log | grep 'Using unknown' | cut -d' ' -f2- | sort | uniq

echo
echo
echo "Warning Summary:"
cat wadl2swagger.log | grep 'WARNING:' | sort | uniq
