function fail_unless_expected {
  file="${1}"
  patterns=("${@}")
  allowed_to_fail=false
  for pattern in $patterns; do
    if [[ "$file" == *"$pattern"* ]]; then
      allowed_to_fail=true
    fi
  done

  if [ "$allowed_to_fail" = true ]; then
    echo $file failed but will not fail the build... this file has known issues that need to be addressed in the wadl
  else
    echo $file failed
    exit 1
  fi
}

function build_wadls {
  VENDOR=$1
  ALLOWED_FAILURE_PATTERNS=$2

  mkdir -p "$VENDOR/swagger"

  pushd $VENDOR
    # Simple conversion:
    # wadl2swagger --autofix wadls/*.wadl -f json

    # But if we want separate log files:
    for wadl in wadls/*.wadl; do
      basename=${wadl##*/}
      basename=${basename%.wadl}
      log_file="swagger/${basename}_log.txt"
      wadl2swagger --autofix $wadl -f json -l $log_file
      if [ $? -ne 0 ]; then
        fail_unless_expected "$wadl" "${ALLOWED_FAILURE_PATTERNS[@]}"
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
}
