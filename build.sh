#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob globstar

pylint application.py ga4gh/drs/server.py || true

exit 0
