#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob globstar

if [[ -z ${BRANCH_NAME+x} ]]; then
    BRANCH_NAME=$(git symbolic-ref --short HEAD)
fi

if [[ -z ${GIT_COMMIT+x} ]]; then
    GIT_COMMIT=$RANDOM
fi

PORT=$((RANDOM+1024))
NAME="${BRANCH_NAME}_${GIT_COMMIT:0:6}"

echo "Running docker image $NAME, listening on host port $PORT"
docker run -t --name "$NAME" -p $PORT:80 drs &
sleep 5

CID=$(docker ps -q --filter "name=$NAME")
echo "containter is $CID"

out=$(curl http://localhost:$PORT/)

docker kill "$CID"

if [[ "$out" = "Hello World!" ]]; then
    echo "OK"
else
    exit 1
fi

# http://.../wsgi -> "Hello World!"

exit 0
