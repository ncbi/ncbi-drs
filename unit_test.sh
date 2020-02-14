#!/usr/bin/env bash

set -euo pipefail
shopt -s nullglob globstar

echo "Starting unit tests"

if [[ -z ${BRANCH_NAME+x} ]]; then
    BRANCH_NAME="none"
fi

if [[ -z ${GIT_COMMIT+x} ]]; then
    GIT_COMMIT="none"
fi

PORT=$((RANDOM+1024))
LOG="/tmp/uwsgi_$USER.log"
rm -f "$LOG"

# Unit tests
echo "Running unit tests"
python3 -m unittest ga4gh/drs/*.py -v
nosetests

#~/.local/bin/uwsgi --http ":$PORT" --wsgi-file drs.py &
uwsgi --logto "$LOG" --http ":$PORT" --wsgi-file drs.py &

sleep 2
RET=0
out=$(curl -s http://localhost:$PORT/)

if [[ "$out" =~ "Hello, Apache!" ]]; then
    echo "1 OK"
else
    echo "1 Failed: $out"
    RET=1
fi

out=$(curl -s -H 'Authorization: authme' http://localhost:$PORT/ga4gh/drs/v1/objects/SRR000000.f4.m.liv.DMSO1.rna.merged.sorted.bam | jq -S '.')
if [[ "$out" =~ "02b1ea5174fee52d14195fd07ece176a" ]]; then
    echo "2 OK results were: $out"
else
    echo "2 Test failed: $out"
    RET=1
fi

out=$(curl -s http://localhost:$PORT/proxy | jq -S '.status' )
if [[ "$out" = "404" ]]; then
    echo "3 OK"
else
    echo "3 Test failed: $out"
    RET=1
fi

echo "Killing uwsgi"
kill %1

# Run mock server
# connexion run openapi/data_repository_service.swagger.yaml --mock=all -v

if [[ "$RET" -ne 0 ]]; then
    echo "See $LOG for details"
fi

echo "Unit tests complete"

exit $RET
