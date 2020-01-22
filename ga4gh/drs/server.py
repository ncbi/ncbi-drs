import connexion
import logging
from datetime import datetime

# from connexion import NoContent
from flask import make_response, abort


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


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
    ret["id"] = "id goes here"
    ret["name"] = "name goes here"
    ret["size"] = 12345
    ret["created_time"] = "1990-12-31T23:59:60Z"
    csum = {"checksum": "FFFFFFF", "type": "crc32c"}
    ret["checksums"] = [csum]

    return ret


def GetAccessURL(object_id: str, access_id: str):
    logging.info(f"In GetAccessURL {object_id} {access_id}")
    logging.info(f"params is {connexion.request.json}")
    logging.info(f"query is {connexion.request.args}")
    ret["url"] = "http://gohere"
    ret["headers"] = ["foo", "bar"]

    return ret


def read():
    logging.info(f"In read()")
    return []
