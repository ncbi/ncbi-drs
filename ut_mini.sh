#!/usr/bin/env bash

LOG="/tmp/uwsgi_$USER.log"
rm -f "$LOG"

# echo "Starting uwsgi"
UWSGI=`which uwsgi`
echo "Starting uwsgi ($UWSGI)"

PORT=$((RANDOM+1024))
#~/.local/bin/uwsgi --http ":$PORT" --wsgi-file drs.py &
echo ${UWSGI} --logto "$LOG" --http ":$PORT" --wsgi-file drs.py
${UWSGI} --logto "$LOG" --http ":$PORT" --wsgi-file drs.py & sleep 2

RET=0

if [[ -z "$TOKEN_FILE" ]]; then
    out=$(curl -s http://localhost:$PORT/ga4gh/drs/v1/objects/SRR000000.f4.m.liv.DMSO1.rna.merged.sorted.bam | jq -S '.')
    if [[ "$out" =~ "02b1ea5174fee52d14195fd07ece176a" ]]; then
        echo "OK results were: $out"
    else
        echo "Test failed: $out"
        RET=1
    fi
else
    out=$(curl -s -H "Authorization: Bearer $(cat $TOKEN_FILE)" http://localhost:$PORT/ga4gh/drs/v1/objects/SRR1219879 | jq -S '.')
    echo "Results were: $out"
fi

echo "Stopping uwsgi"
kill %1

# Run mock server
# connexion run openapi/data_repository_service.swagger.yaml --mock=all -v

if [[ "$RET" -eq 0 ]]; then
    echo "Unit tests complete"
    exit 0
fi

echo "See $LOG for details"
cat $LOG
exit 1
