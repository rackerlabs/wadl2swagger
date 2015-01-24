#!/bin/bash
rm -rf site/source/rackspace
rm -rf site/source/openstack

cp -r rackspace site/source/
rm -rf openstack/openstack-api-site
cp -r openstack site/source/

cp README.md site/source/index.md
pushd site
  rm -rf build/
  bundle install
  # bundle exec thor yaml2json
  bundle exec thor json2yaml
  bundle exec middleman build
popd
