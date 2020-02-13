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
import requests
import flask

from .rewrite import Rewriter
from .cloud import ComputeEnvironmentToken

from urllib.parse import urlsplit, urlunsplit, urljoin

_rewriter = Rewriter()


def generate(resp):
    try:
        total = resp.headers["Content-Length"]
        BufSize = 4096 * 1024
        for chunk in resp.iter_content(BufSize):
            yield chunk
    except Exception as ex:
        return "generate() threw " + str(ex)
    return


def redirect(url: str, _headers):
    # https://host:port/proxy/12345

    # replace "host:port/proxy" with redirectURL
    (scheme, netloc, path, *dummy) = urlsplit(url)
    shortID = path[7:]  # whatever is after "proxy/"
    if not shortID:
        return {"status_code": 200, "msg": "here be proxy"}

    redirectorURL = _rewriter.Retrieve(shortID)
    if not redirectorURL:
        return {"status_code": 404, "msg": "Accession is not found"}  # is this correct?

    # POST to the redirector with ident=CE
    redir = requests.post(
        redirectorURL, data={"ident": ComputeEnvironmentToken()}, allow_redirects=False
    )

    # intercept a redirect, capture the temporary signed bucket URL and its expiration
    if redir.status_code == 307:
        try:
            bucketUrl = redir.headers["Location"]
            expiration = redir.headers["Expires"]

            # send request to bucket server
            resp = requests.get(bucketUrl, stream=True)

            return flask.Response(flask.stream_with_context(generate(resp)))

        #            return "data\n", resp.status_code, resp.headers.items()
        #            return resp.raw.read(), resp.status_code, resp.headers.items()

        except Exception as ex:
            # TODO: return something more appropriate
            return {"status_code": 200, "msg": str(ex)}

    # TODO: sanitize the unexpected response from the redirector
    return redir.text, redir.status_code, redir.headers.items()


def do_proxy(request):
    return redirect(connexion.request.url, request.headers)


# --------------------- Unit tests

import unittest


class TestServer(unittest.TestCase):

    # test cases

    def test_Proxy_BadAcc(self):
        res = redirect("https://localhost:80/proxy/blah", [])
        print(res)

    #        self.assertEqual(404, res['status_code']) # is 404 correct?

    def test_Proxy_BadJwt(self):
        # TODO: a working jwt
        shortID = _rewriter.Rewrite(
            "https://locate.ncbi.nlm.nih.gov/sdlr/sdlr.fcgi?jwt=eyJ"
        )
        res = redirect("https://localhost:80/proxy/" + shortID, [])
        print(res)


#        self.assertEqual(501, res['status_code'])


if __name__ == "__main__":
    unittest.main()
