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

"""
   This module defines a transparent HTTP proxy for the NCBI's DRS webservice
"""

import requests
import flask
import logging
import sys
import os
from urllib.parse import urlsplit, urlunsplit, urljoin

try:
    from .rewrite import Rewriter
    from .cloud import ComputeEnvironmentToken
except:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from rewrite import Rewriter
    from cloud import ComputeEnvironmentToken

_rewriter = Rewriter()


_CHUNK_SIZE = 10 * 1024 * 1024  # 10MB


def _streamContent(resp: requests.Response):
    """ Generator function, iterates over the content of a requests.Response in _CHUNK_SIZE chunks

       Parameters
       ----------
       resp: request.Response to be iterated

       Returns
       -------
       yields the next chunk (bytes, <= _CHUNK_SIZE long) of the response's,
       or returns if there is no more or an exception has occurred

    """

    try:
        for chunk in resp.iter_content(_CHUNK_SIZE):
            yield chunk
    except Exception as ex:
        logging.error("streamContent(): resp.iter_content() threw " + str(ex))
    finally:
        return


def _redirect(shortID: str):
    """ For a given shortID retrieve the coresponding URL to the NCBI redirector service,
        get a temporary signed URL to the target file from the redirector,
        produce a Flask.Response object that can stream the target file

       Parameters
       ----------
       shortID: a key returned by an earlier request to "http://$HOST:$PORT/ga4gh/drs/v1/objects/$ACCESSION"

       Returns
       -------
       a Flask.Response object that can stream the target file

    """

    # retrieve the redirectURL corresponding to the shortID
    redirectorURL = _rewriter.Retrieve(shortID)
    if not redirectorURL:
        return {"status_code": 404, "msg": "Accession is not found"}, 404, {}

    # POST to the redirector with ident=CE
    redir = requests.post(
        redirectorURL, data={"ident": ComputeEnvironmentToken()}, allow_redirects=False
    )

    # intercept a redirect, capture the temporary signed bucket URL
    if redir.status_code == 307:
        try:
            bucketUrl = redir.headers["Location"]
            # expiration = redir.headers["Expires"]

            # send request to bucket server, ready to stream the data
            resp = requests.get(bucketUrl, stream=True)

            # this will start streaming
            ret = flask.Response(flask.stream_with_context(_streamContent(resp)))
            ret.content_type = resp.headers["Content-Type"]
            ret.content_length = resp.headers["Content-Length"]

            return ret

        except Exception as ex:
            return {"status_code": 500, "msg": str(ex)}, 500, {}

    return {
        "status_code": 501,
        "msg": f"unexpected response from redirector: {redir.status_code} {redir.reason}",
    }, 501, {}


def do_proxy(shortID: str):
    """ For a given shortID retrieve the coresponding URL to the NCBI redirector service,
        get a temporary signed URL to the target file from the redirector,
        produce a Flask.Response object that can stream the target file

       Parameters
       ----------
       shortID: a key returned by an earlier request to "http://$HOST:$PORT/ga4gh/drs/v1/objects/$ACCESSION"

       Returns
       -------
       a Flask.Response object that can stream the target file

    """
    return _redirect(shortID)


# --------------------- Unit tests

import unittest


class _TestProxy(unittest.TestCase):

    # test cases

    def test_Proxy_BadAcc(self):
        (res, *dummy) = _redirect("blah")
        # print(res)
        self.assertEqual(404, res["status_code"])  # is 404 correct?

    # def test_Proxy_BadJwt(self):
    #     # TODO: a working jwt
    #     shortID = _rewriter.Rewrite(
    #         "https://locate.ncbi.nlm.nih.gov/sdlr/sdlr.fcgi?jwt=eyJ"
    #     )
    #     res = _redirect(shortID)
    #     print(res)
    #     self.assertEqual(404, res['status_code'])


if __name__ == "__main__":
    unittest.main()
