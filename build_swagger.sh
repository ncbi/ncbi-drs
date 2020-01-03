#!/bin/bash

set -o nounset # same as -u
set -o errexit # same as -e
set -o pipefail
shopt -s nullglob globstar

java \
    -jar "$HOME/swagger-codegen/modules/swagger-codegen-cli/target/swagger-codegen-cli.jar" \
    generate \
    -i https://raw.githubusercontent.com/ga4gh/data-repository-service-schemas/master/openapi/data_repository_service.swagger.yaml \
    -l python-flask \
    -o "$HOME/ncbi-drs/swagger"
