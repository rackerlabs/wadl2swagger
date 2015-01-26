#!/usr/bin/env bash
ALLOWED_FAILURE_PATTERNS=("os-object-api-1.0" "identity-admin-v3" "os-image-1.0" "security-groups" "identity-admin")
SCRIPTDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
source $SCRIPTDIR/build_wadls.sh

build_wadls "openstack" "${ALLOWED_FAILURE_PATTERNS[@]}"
