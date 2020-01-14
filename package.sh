#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob globstar

docker build -t drs .

exit 0
