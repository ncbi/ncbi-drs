#!/usr/bin/env python3

from flask import render_template
import connexion
import getpass
import logging

logging.basicConfig(level=logging.INFO)

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
    if username == "admin" and password == "secret":
        return {"sub": "admin"}

    # optional: raise exception for custom error response
    return None


def get_secret(user) -> str:
    return "You are {user} and the secret is 'wbevuec'".format(user=user)


# Create a URL route in our application for "/"
@app.route("/")
def home():
    """
    This function just responds to the browser URL
    localhost:5000/
    :return:        the rendered template 'home.html'
    """
    username = getpass.getuser()
    # connexion.request.method
    return render_template("home.html", title="DRS", user=username)


# def application(environ, start_response):
#    status = "200 OK"
#    output = b"Hello World!"
#
#    response_headers = [
#        ("Content-type", "text/plain"),
#        ("Content-Length", str(len(output))),
#    ]
#    start_response(status, response_headers)
#
#    return [output]


# If we're running in stand alone mode, run the application
if __name__ == "__main__":
    app.run(port=4772, debug=True)
