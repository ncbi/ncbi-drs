#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob globstar

if [[ -z ${BRANCH_NAME+x} ]]; then
    BRANCH_NAME="none"
fi

if [[ -z ${GIT_COMMIT+x} ]]; then
    GIT_COMMIT="none"
fi

PORT=$((RANDOM+1024))
echo "Running docker image, listening on host port $PORT"

#docker run --name ga4gh -p 443:80 drs
docker run -t --name "${BRANCH_NAME}_${GIT_COMMIT:0:6}" -p $PORT:80 drs &
sleep 5

out=$(curl http://localhost:443/)
if [[ "$out" = "Hello World!" ]]; then
    echo "OK"
else
    exit 1
fi

# http://.../wsgi -> "Hello World!"

exit 0
