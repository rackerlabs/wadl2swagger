#!/bin/bash
pushd site
bundle exec middleman deploy
popd
