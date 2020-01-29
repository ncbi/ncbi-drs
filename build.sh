#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob globstar

type -a protoc
type -a black
type -a pylint

# pip3 install -r requirements.txt -r test-requirements.txt

protoc --python_out=ncbi/pb ncbi/ncbi_log.proto

#pre-commit run --all-files
black ncbi/pb/ncbi/ncbi_log_pb2.py

pylint drs.py ga4gh/drs/server.py || true

exit 0
