#!/bin/bash
cp -r wadls site/source/
cp -r swagger site/source
pushd site
rm -rf build/
rm source/swagger/*.json
bundle install
bundle exec thor yaml2json
bundle exec middleman build
popd
