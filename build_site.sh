#!/bin/bash
cp -r wadls site/source/
cp -r swagger site/source
pushd site
bundle install
bundle exec middleman build
popd
