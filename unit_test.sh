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
python3 -m unittest ga4gh/drs/server.py
nosetests

#~/.local/bin/uwsgi --http ":$PORT" --wsgi-file drs.py &
uwsgi --logto "$LOG" --http ":$PORT" --wsgi-file drs.py &

sleep 2
RET=0
out=$(curl -s http://localhost:$PORT/)

if [[ "$out" =~ "Hello, Apache!" ]]; then
    echo "OK"
else
    echo "Failed: $out"
    RET=1
fi

out=$(curl -s -H 'Authorization: authme' http://localhost:$PORT/ga4gh/drs/v1/objects/1234 | jq -S '.')
# Should return "md5": "aa8fbf47c010ee82e783f52f9e7a21d0",
if [[ "$out" =~ "aa8fbf47c010ee82e783f52f9e7a21d0" ]]; then
    echo "OK results were: $out"
else
    echo "Test failed: $out"
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
