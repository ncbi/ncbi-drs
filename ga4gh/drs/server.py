import connexion
import logging
import datetime
import requests

# from connexion import NoContent
from flask import make_response, abort

SDL_CGI = "https://locate.ncbi.nlm.nih.gov/sdl/2/retrieve/repository/remote/main/SDL.2/resolver-cgi"


def get_timestamp():
    d = datetime.datetime.utcnow()
    return d.isoformat("T") + "Z"


def apikey_auth(token, required_scopes):
    logging.info(f"Got server apikey {token} {required_scopes}")
    ok = {"uid": 100}
    if False:
        raise OAuthProblem("Invalid token")
    return ok


def GetObject(object_id: str, expand: bool):
    logging.info(f"In GetObject {object_id} {expand}")
    logging.info(f"params is {connexion.request.json}")
    logging.info(f"query is {connexion.request.args}")

    ret = {}

    # Fake request
    sdl = requests.get(SDL_CGI)
    ret["status"] = sdl.status_code
    ret["text"] = sdl.text
    ret["json"] = sdl.json()
    ret["sdl_message"] = sdl.json()["message"]

    ret["id"] = f"id goes here: {object_id}"
    ret["expanded"] = f"expand={expand}"
    ret["self_uri"] = "http://example.com"
    ret["size"] = 12345
    ret["created_time"] = "1990-12-31T23:59:60Z"
    valid_sums = [
        "sha-256",
        "sha-512",
        "sha3-256",
        "sha3-512",
        "md5",
        "etag",
        "crc32c",
        "trunc512",
        "sha1",
    ]
    csum = {"checksum": "FFFFFFF", "type": "crc32c"}
    ret["checksums"] = [csum]

    # Optional fields
    ret["name"] = "name goes here"
    ret["updated_time"] = get_timestamp()
    ret["version"] = "version"
    ret["mime_type"] = "application/json"
    ret["access_methods"] = ["https", "s3", "gs"]
    ret["description"] = "description"
    ret["aliases"] = "aliases"

    return ret


def GetAccessURL(object_id: str, access_id: str):
    logging.info(f"In GetAccessURL {object_id} {access_id}")
    logging.info(f"params is {connexion.request.json}")
    logging.info(f"query is {connexion.request.args}")
    ret["self_uri"] = "http://gohere"
    ret["headers"] = ["foo", "bar"]

    return ret


def read():
    logging.info(f"In read()")
    return []
