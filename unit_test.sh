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
#~/.local/bin/uwsgi --http ":$PORT" --wsgi-file drs.py &
uwsgi --http ":$PORT" --wsgi-file drs.py &

sleep 2
RET=0
out=$(curl http://localhost:$PORT/)

if [[ "$out" =~ "Hello, Apache!" ]]; then
    echo "OK"
else
    echo "Failed: $out"
    RET=1
fi

echo "Killing uwsgi"
kill %1

exit $RET
