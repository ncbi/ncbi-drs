#!/bin/sh
DRS_DB=${TMPDIR}drs.sqlite
cat setup/makedb.sql setup/data.sql | sqlite3 ${DRS_DB}
cat data-repository-service-schemas/openapi/data_repository_service.swagger.yaml | sed 's/ga4gh.drs.server/drs.server/' > src/drs/openapi/data_repository_service.swagger.yaml
TESTING=1 DRS_DB=${DRS_DB} PYTHONPATH=src pytest -v -rsx tests
rm -r ${DRS_DB} src/drs/openapi/data_repository_service.swagger.yaml
