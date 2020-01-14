#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob globstar

docker run -it --name ga4gh -p 443:80 drs
# http://.../wsgi -> "Hello World!"

exit 0
