#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob globstar

docker run -it --name ga4gh -p 443:80 drs

exit 0
