""" Get Cloud Compute Environment Token """

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

import socket
import base64
import requests

def _Base64(val: str) -> str:
    """ Applies Base64 encoding to a string

       Parameters
       ----------
       val : string to be encoded

       Returns
       -------
       base64-encoded val
   """

    b64 = base64.b64encode(val.encode("utf-8"))
    return str(b64, "utf-8")


def _GetAWS_CE() -> str:
    """ Get Compute Environment for AWS """
    try:  # AWS
        AWS_INSTANCE_URL = "http://169.254.169.254/latest/dynamic/instance-identity"

        document = requests.get(AWS_INSTANCE_URL + "/document")
        if document.status_code == requests.codes.ok:
            # encode the components
            doc_b64 = _Base64(document.text)
            pkcs7 = requests.get(AWS_INSTANCE_URL + "/pkcs7")
            pkcs7_b64 = _Base64(
                "-----BEGIN PKCS7-----\n" + pkcs7.text + "\n-----END PKCS7-----\n"
            )

            return doc_b64 + "." + pkcs7_b64
    except:
        pass

    return None


def _GetGCP_CE() -> str:
    """ Get Compute Environment for GCP """
    try:  # GCP
        GCP_CE_URL = (
            "http://metadata/computeMetadata/v1/instance/service-accounts/default/identity"
            "?audience=https://www.ncbi.nlm.nih.gov&format=full"
        )
        document = requests.get(GCP_CE_URL, headers={"Metadata-Flavor": "Google"})
        if document.status_code == requests.codes.ok:
            return document.text
    except:
        pass

    return None


def _GetCloud():
    """ Discover Cloud by trying to access platform-specific metadata

       Parameters
       ----------
       none

       Returns
       -------
       Function for getting the Compute Environment or None
    """
    try:
        """ GCP has this hostname """
        HOSTNAME = "metadata"
        socket.gethostbyname(HOSTNAME)
        return _GetGCP_CE
    except:
        pass

    try:
        """ Try connecting to AWS metadata server
            It should connect immediately if in AWS
        """
        HOST = "169.254.169.254"
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.100)
        sock.connect((HOST, 80))
        sock.close()
        return _GetAWS_CE
    except:
        pass
    finally:
        sock.close()

    return None


_cloud = _GetCloud()

def ComputeEnvironmentToken() -> str:
    """Returns a Computing Environment token specifying the current cloud context (AWS, GCP, or neither).
       The CE token is to be sent to SDL as "ident=<CEtoken>" in the body of a POST request.

       Parameters
       ----------
       none

       Returns
       -------
       CE token as a string if on a cloud, or None if not on a cloud.
    """

    return _cloud() if _cloud else None


_verbose = None

import unittest

class TestServer(unittest.TestCase):
    def _OnGCP(self):
        return _cloud == _GetGCP_CE

    def _OnAWS(self):
        return _cloud == _GetAWS_CE

    # test cases

    def test_GetCE_docstring(self):
        # make sure has a docstring
        self.assertTrue(ComputeEnvironmentToken.__doc__)

    def test_GetCE(self):
        # output on the current platform
        s = ComputeEnvironmentToken()

        if self._OnGCP():
            # an instance identity token, base64url-encoded
            if _verbose:
                print("GCP detected")
            self.assertNotEqual(s, "")

        elif self._OnAWS():
            # a base64-encoded Instance Identity Document (Json) followed by "." and a base64-encoded pkcs7 signature
            if _verbose:
                print("AWS detected")
            self.assertNotEqual(s.find("."), -1)

        else:
            # neither AWS nor GCP: empty
            if _verbose:
                print("no cloud detected")
            self.assertEqual(s, None)

import sys

if __name__ == "__main__":
    _verbose = "--verbose" in sys.argv
    unittest.main()
