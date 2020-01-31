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
NAME="${BRANCH_NAME}_${GIT_COMMIT:0:6}_$RANDOM"

echo "Running docker image $NAME, listening on host port $PORT"
docker run --network=host -d --name "$NAME" -p $PORT:80 drs
sleep 15

CID=$(docker ps -q --filter "name=$NAME")
echo "container is $CID"

set +e
date
RET=0
echo curl -s http://localhost:$PORT/
curl -s http://localhost:$PORT/
out=$(curl -s http://localhost:$PORT/ || true)
CURLRET=$?
date

if [[ "$out" =~ "Hello, Apache!" ]]; then
    echo "OK"
else
    echo "curl returned $CURLRET"
    echo "Failed: '$out'"
    RET=1
fi

out=$(curl -s -H 'Authorization: authme' http://localhost:$PORT/ga4gh/drs/v1/objects/1234 | jq -S '.')
echo "Received: '$out'"

if [[ "$RET" -ne 0 ]]; then
    echo "Logs"
    echo "----"
    docker exec -t "$NAME" /usr/bin/tail -n 20 /var/log/apache2/error.log /tmp/drs_app.log
    echo "----"
fi


echo "Killing docker image"
exit 0
docker kill "$CID"
docker container rm "$CID"

exit $RET
