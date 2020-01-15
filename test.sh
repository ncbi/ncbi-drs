#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob globstar

if [[ -z ${BRANCH_NAME+x} ]]; then
    BRANCH_NAME="none"
fi

if [[ -z ${GIT_COMMIT+x} ]]; then
    GIT_COMMIT="none"
fi

#docker run --name ga4gh -p 443:80 drs
docker run -t "${BRANCH_NAME}_${GIT_COMMIT:0:6}" -p 443:80 drs
# http://.../wsgi -> "Hello World!"

exit 0
