#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob globstar

if [[ -z ${BRANCH_NAME+x} ]]; then
    BRANCH_NAME=$(git symbolic-ref --short HEAD)
fi

if [[ -z ${GIT_COMMIT+x} ]]; then
    GIT_COMMIT=$RANDOM
fi

#PORT=$((RANDOM+1024))
PORT=80
NAME="${BRANCH_NAME}_${GIT_COMMIT:0:6}_$RANDOM"

#docker network create test-network
echo "Running docker image $NAME, listening on host port $PORT"
#docker run --network test-network --detach --name "$NAME" --publish $PORT:80 drs
docker run --network host --detach --name "$NAME" drs
sleep 5

CID=$(docker ps -q --filter "name=$NAME")
echo "container is $CID"

set +e
RET=0
echo curl -s http://localhost:$PORT/
#curl -s http://localhost:$PORT/
out=$(curl -s http://localhost:$PORT/ || true)
CURLRET=$?

if [[ "$out" =~ "Hello, Apache!" ]]; then
    echo "OK"
else
    echo "curl returned $CURLRET"
    echo "Failed: '$out'"
    RET=1
fi

out=$(curl -s -H 'Authorization: authme' http://localhost:$PORT/ga4gh/drs/v1/objects/SRR000000.f4.m.liv.DMSO1.rna.merged.sorted.bam | jq -S '.')
if [[ "$out" =~ "02b1ea5174fee52d14195fd07ece176a" ]]; then
    echo "OK"
else
    echo "Test failed: $out"
    RET=1
fi

if [[ "$RET" -ne 0 ]]; then
    echo "Logs"
    echo "----"
    docker exec -t "$NAME" /usr/bin/tail -n 20 /var/log/apache2/error.log /tmp/drs_app.log
    echo "----"
fi

echo "Killing docker image"
docker kill "$CID"
docker container rm "$CID"
#docker network rm test-network

echo "RET is $RET"
exit $RET
