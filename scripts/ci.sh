#!/bin/bash
set -e

if [ "$CI" = "true" ]; then
  # We're on Snap-CI, Travis, etc.
  sudo npm install -g swagger-tools
  sudo yum install --assumeyes pandoc
  python setup.py install
else
  python setup.py develop
fi

SCRIPTDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

$SCRIPTDIR/fetch_rackspace_wadls.sh
$SCRIPTDIR/fetch_openstack_wadls.sh

$SCRIPTDIR/build_rackspace_wadls.sh
$SCRIPTDIR/build_openstack_wadls.sh

echo "Unknown types summary:"
find rackspace openstack -name \*_log.txt | xargs grep 'Unknown type' | cut -d' ' -f2- | sort | uniq

echo
echo
echo "Warning Summary:"
find rackspace openstack -name \*_log.txt | xargs grep 'WARNING:' | sort | uniq
