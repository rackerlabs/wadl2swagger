#!/usr/bin/env bash
mkdir -p rackspace/wadls
pushd rackspace
wadlcrawler http://api.rackspace.com/wadls/
rm wadls/email*.wadl # Skip mailgun WADLs
# rm wadls/cloud_monitoring.wadl # Is monitoring clean yet?
popd
