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
import datetime
import logging
import requests
import unittest

# from connexion import NoContent
from flask import make_response, abort

SDL_CGI = "https://locate.ncbi.nlm.nih.gov/sdl/2/retrieve"

VALID_CHECKSUMS = [
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

VALID_ACCESS_METHODS = [
    "s3",
    "gs",
    "ftp",
    "gsiftp",
    "globus",
    "htsget",
    "https",
    "file",
]


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

    # TODO: Confirm object_id matches [A-Za-z0-9.-_~]+

    sdl = requests.post(
        SDL_CGI, data={"acc": "SRR10039049", "accept-proto": "https", "filetype": "bam"}
    )
    #    sdl = requests.post(SDL_CGI)
    ret["sdl_status"] = sdl.status_code
    ret["sdl_json"] = sdl.json()
    # ret["sdl_result"] = sdl.json()["result"]

    csum = {"checksum": "FFFFFFF", "type": "crc32c"}
    if csum["type"] not in VALID_CHECKSUMS:
        logging.error("invalid checksum " + csum["type"])

    ret["checksums"] = [csum]

    # Optional fields
    # ret["name"] = "name goes here"
    # ret["updated_time"] = get_timestamp()
    # ret["version"] = "version"
    # ret["mime_type"] = "application/json"
    # ret["access_methods"] = ["https", "s3", "gs"]
    # ret["description"] = "description"
    # ret["aliases"] = "aliases"

    return ret


def GetAccessURL(object_id: str, access_id: str):
    logging.info(f"In GetAccessURL {object_id} {access_id}")
    logging.info(f"params is {connexion.request.json}")
    logging.info(f"query is {connexion.request.args}")

    ret = {}

    # TODO: Confirm object_id matches [A-Za-z0-9.-_~]+
    # TODO: Confirm access_id is in VALID_ACCESS_METHODS (connexion does?)
    ret["self_uri"] = "http://gohere"
    ret["headers"] = ["foo", "bar"]

    return ret


class TestServer(unittest.TestCase):
    # TODO: Not very useful without rest of HTTP/Connexion framework
    def test_Bogus(self):
        self.assertTrue(True)


def read():
    logging.info(f"In read()")
    return []


if __name__ == "__main__":
    unittest.main()
