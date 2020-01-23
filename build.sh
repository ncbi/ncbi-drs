#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob globstar

protoc --python_out=ncbi/pb ncbi/ncbi_log.proto

pylint drs.py ga4gh/drs/server.py || true

exit 0
