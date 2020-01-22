#!/usr/bin/env python3

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
app.add_api("data_repository_service.swagger.yaml", strict_validation=False)  # FIXME

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


# If we're running in stand alone mode, run the application
if __name__ == "__main__":
    logger.info("in main")
    app.run(port=20814, debug=True)
