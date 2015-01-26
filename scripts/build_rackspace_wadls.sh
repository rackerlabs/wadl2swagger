#!/usr/bin/env bash

ALLOWED_FAILURE_PATTERNS=("cloud_monitoring" "email" "identity-admin")
SCRIPTDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
source $SCRIPTDIR/build_wadls.sh

build_wadls "rackspace" "${ALLOWED_FAILURE_PATTERNS[@]}"
