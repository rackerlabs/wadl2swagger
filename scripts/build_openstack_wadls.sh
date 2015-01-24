#!/usr/bin/env bash

function fail_unless_expected {
  echo $1
  if [[ "$1" == *"os-object-api-1.0.wadl"* ]] || [[ "$1" == *"identity-admin-v3.wadl"* ]] || [[ "$1" == *"os-image-1.0.wadl"* ]] || [[ "$1" == *"security-groups.wadl"* ]]; then
    echo $1 failed but will not fail the build... this file has known issues that need to be addressed in the wadl
  else
    echo $1 failed
    exit 1
  fi
}

# Remove WADLs with known issues - should be corrected
  rm wadls/os-object-api-1.0.wadl
  rm wadls/identity-admin-v3.wadl
  rm wadls/os-image-1.0.wadl
  rm wadls/security-groups.wadl


pushd openstack
  # Simple conversion:
  # wadl2swagger --no-doc --autofix wadls/*.wadl

  # But if we want separate log files:
  for wadl in wadls/*.wadl; do
    basename=${wadl%.wadl}
    wadl2swagger --no-doc --autofix $wadl -l "$basename.log"
    if [ $? -ne 0 ]; then
      fail_unless_expected $wadl
    fi
  done
popd
