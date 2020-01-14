#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob globstar

env

docker build -t drs .

exit 0
