#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob globstar

docker run -dit --name ga4gh -p 20814:80 drs

exit 0
