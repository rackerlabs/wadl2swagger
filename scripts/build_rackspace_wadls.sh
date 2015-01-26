#!/usr/bin/env bash

# wadl2swagger blows up trying to convert these files, but because the WADLs contain issues
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
  # wadl2swagger --autofix wadls/*.wadl -f json

  # But if we want separate log files:
  for wadl in wadls/*.wadl; do
    basename=${wadl##*/}
    basename=${basename%.wadl}
    log_file="swagger/${basename}.log"
    wadl2swagger --autofix $wadl -f json -l $log_file
    if [ $? -ne 0 ]; then
      fail_unless_expected $wadl
    fi
    echo >> $log_file
    echo "Validating with swagger-tools..." >> $log_file
    swagger-tools validate "swagger/$basename.json" 2>&1 | tee -a $log_file

    case "${PIPESTATUS[0]}" in
      "0")
        echo "Valid" >> $log_file
        ;;
      "1")
        echo "Invalid" >> $log_file
        ;;
      *)
        echo "Error (exit code ${PIPESTATUS[0]})" >> $log_file
        ;;
    esac
  done
popd
