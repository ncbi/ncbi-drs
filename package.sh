#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob globstar

docker build --pull --no-cache --tag drs .

exit 0
