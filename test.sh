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

RET=0
out=$(curl http://localhost:$PORT/)

if [[ "$out" =~ "Hello, Apache!" ]]; then
    echo "OK"
else
    echo "Failed: $out"
    docker exec -it "$NAME" /usr/bin/tail -20 /var/log/apache2/error.log
    RET=1
fi

echo "Killing docker image"
docker kill "$CID"

exit $RET
