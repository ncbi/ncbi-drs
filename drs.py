#!/usr/bin/env python3

import connexion
import logging
import sys
from flask import render_template

# import getpass

sys.path.append("/var/www/wsgi-scripts/")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
f_handler = logging.FileHandler("drs_app.log")
f_handler.setLevel(logging.DEBUG)
f_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)

logger.info("logging started")
# logging.basicConfig(level=logging.INFO)

# Create the application instance
options = {
    "serve_spec": False,  # Don't show spec JSON
    "swagger_ui": False,
}  # Don't show swagger console

app = connexion.App(__name__, options=options, specification_dir="./openapi")

# Read the swagger.yml file to configure the endpoints
app.add_api("data_repository_service.swagger.yaml", strict_validation=True)

application = app.app


def basic_auth(username, password, required_scopes=None):
    logger.warn(f"basic_auth {username} {password}")
    if username == "admin" and password == "secret":
        return {"sub": "admin"}

    # optional: raise exception for custom error response
    return None


def get_secret(user) -> str:
    logger.warn(f"get_secret {user}")
    return "You are {user} and the secret is 'wbevuec'".format(user=user)


# Create a URL route in our application for "/"
@app.route("/")
def home():
    """
    This function just responds to the browser URL
    localhost:5000/
    :return:        the rendered template 'home.html'
    """
    username = "Apache"  # getpass.getuser()
    logger.warn(f"Got {username}")
    # connexion.request.method
    return render_template("home.html", title="DRS", username=username)


# If we're running in stand alone mode, run the application
if __name__ == "__main__":
    logger.warning("in main")
    app.run(port=4772, debug=True)
