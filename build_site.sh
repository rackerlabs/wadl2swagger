#!/bin/bash
rm -rf site/source/rackspace
rm -rf site/source/openstack

cp -r rackspace site/source/
cp -r openstack/wadls site/source/openstack
cp -r openstack/swagger site/source/openstack

cp README.md site/source/index.html.md
pushd site
rm -rf build/
bundle install
bundle exec thor yaml2json
bundle exec middleman build
popd
