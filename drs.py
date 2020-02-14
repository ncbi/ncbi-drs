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


import connexion
import logging
import os
import sys
from flask import render_template

sys.path.append("/var/www/wsgi-scripts/")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
f_handler = logging.FileHandler("/tmp/drs_app.log")
f_handler.setLevel(logging.DEBUG)
f_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)

if "NCBI_LOGGER" in os.environ:
    from ncbi import logger

    logger.addHandler()


logger.info(f"logging started: {__name__}")
# logging.basicConfig(level=logging.INFO)

# Create the application instance
options = {
    "serve_spec": False,  # Don't show spec JSON
    "swagger_ui": False,
}  # Don't show swagger console

os.environ["APIKEYINFO_FUNC"] = "ga4gh.drs.server.apikey_auth"

app = connexion.App(__name__, options=options, specification_dir="./openapi")

# Read the swagger.yml file to configure the endpoints
# TODO: validate=True
app.add_api("data_repository_service.swagger.yaml", strict_validation=True)

application = app.app


# Create a URL route in our application for "/"
@app.route("/")
def home():
    """
    This function just responds to the browser URL
    localhost:5000/
    :return:        the rendered template 'home.html'
    """
    username = "Apache"  # getpass.getuser()
    logger.info(f"Got {username}")
    logger.info(f"headers is {connexion.request.headers}")
    logger.info(f"params is {connexion.request.json}")
    logger.info(f"query is {connexion.request.args}")
    # connexion.request.method
    return render_template("home.html", title="DRS", username=username)


# --------------------- proxy
from ga4gh.drs.proxy import do_proxy


@app.route("/proxy/<shortID>")
def proxy(shortID):
    return do_proxy(shortID)


# ---------------------

# If we're running in stand alone mode, run the application
if __name__ == "__main__":
    logger.info("in main")
    app.run(port=20814, debug=True)
