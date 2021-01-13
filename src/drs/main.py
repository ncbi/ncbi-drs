#!/usr/bin/env python3
# =============================================================================
#
#                            PUBLIC DOMAIN NOTICE
#               National Center for Biotechnology Information
#
#  This software/database is a "United States Government Work" under the
#  terms of the United States Copyright Act.  It was written as part of
#  the author's official duties as a United States Government employee and
#  thus cannot be copyrighted.  This software/database is freely available
#  to the public for use. The National Library of Medicine and the U.S.
#  Government have not placed any restriction on its use or reproduction.
#
#  Although all reasonable efforts have been taken to ensure the accuracy
#  and reliability of the software and data, the NLM and the U.S.
#  Government do not and cannot warrant the performance or results that
#  may be obtained by using this software or data. The NLM and the U.S.
#  Government disclaim all warranties, express or implied, including
#  warranties of performance, merchantability or fitness for any particular
#  purpose.
#
#  Please cite the author in any work or product based on this material.
#
# =============================================================================


import logging.config
import os

import connexion
from flask import make_response, Response, send_from_directory

logLevel = 'INFO'  # 'WARNING'
try:
    if 'DEBUG' in os.environ['DRS_LOGGING'].split():
        logLevel = 'DEBUG'
except KeyError:
    pass

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
}

logging.config.dictConfig(LOGGING)

logger = logging.getLogger(__name__)
logger.info(f"logging started: {__name__}")

# Create the application instance
options = {
    "serve_spec": True,
    "swagger_ui": False,
}

os.environ["APIKEYINFO_FUNC"] = "drs.server.apikey_auth"

app = connexion.App(__name__, options=options, specification_dir="./openapi")

swagger_yml = 'data_repository_service.swagger.yaml'
app.add_api(swagger_yml, strict_validation=True)

application = app.app


# Create a URL route in our application for "/"
@app.route("/health/")
def health_check():
    return make_response(Response(''), 200)


@app.route("/ga4gh/drs/v1/")
def home():
    return send_from_directory('./openapi', 'index.html')


# Create a URL route in our application for "/"
@app.route("/")
def root_check():
    return make_response(Response('ok'), 200)


# ---------------------
def main_doc(in_val: int) -> int:
    return in_val
