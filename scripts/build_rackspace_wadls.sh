#!/usr/bin/env bash

function fail_unless_expected {
  echo $1
  if [[ "$1" == *"cloud_monitoring"* ]] || [[ "$1" == *"email"* ]] ; then
    echo $1 failed but will not fail the build... this file has known issues that need to be addressed in the wadl
  else
    echo $1 failed
    exit 1
  fi
}

pushd rackspace
  # Simple conversion:
  wadl2swagger --no-doc --autofix wadls/*.wadl -f json

  # But if we want separate log files:
  # for wadl in wadls/*.wadl; do
  #   basename=${wadl%.wadl}
  #   wadl2swagger --autofix $wadl -l "$basename.log" -f json
  #   # Requires swagger-tools... npm install -g swagger-tools
  #   # swagger-tools validate $basename.yaml
  #   if [ $? -ne 0 ]; then
  #     fail_unless_expected $wadl
  #   fi
  # done
popd
