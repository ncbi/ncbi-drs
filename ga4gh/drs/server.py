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
import re
import socket
import base64
import json
import hashlib

# from connexion import NoContent
from flask import make_response, abort

SDL_RETRIEVE_CGI = "https://locate.ncbi.nlm.nih.gov/sdl/2/retrieve"
SDL_LOCALITY_CGI = "https://locate.ncbi.nlm.nih.gov/sdl/2/locality"

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

def _GetRedirURL(location):
    return location['link']

def _TranslateService(location):
    try: return { 's3': 's3', 'gs': 'gs' }[location['service']]
    except: return 'https'

def _MakeAccessMethod(location):
    """ Create a DRS Access Method from SDL info """
    access_method = { 'access_url': _GetRedirURL(location), 'type': _TranslateService(location) }
    if location.get('region'):
        access_method['region'] = location.get('region')
    return access_method

### @brief _ParseSDLResponseV2 Parse version 2 SDL response JSON
###
### @param response: SDL response JSON
### @param query: { bundle: accession, type: file type }
###
### @return None if error else Dictionary with requested object or a 404
def _ParseSDLResponseV2(response, accession: str, file_part: str):
    """ Parse version 2 SDL Response JSON """
    for result in response['result']:
        if result['bundle'] != accession: continue

        msg = result.get('msg')
        status = str(result['status'])
        if status != '200':
            yield {'status': status, 'msg': msg}
            return

        for file in result['files']:
            name = file['name']
            access_methods = None
            if file_part:
                if file_part != name: continue
                access_methods = list(_MakeAccessMethod(location) for location in file['locations'])

            yield {
                'status': '200',
                'msg': msg,
                'id': f"{accession}.{name}",
                'name': name,
                'size': file['size'],
                'md5': file['md5'],
                'date': file['modificationDate'],
                'access_methods': access_methods
            }

### @brief _ParseSDLResponse Parse SDL response JSON
###
### @param response: SDL response JSON
### @param accession: the query accession
### @param file_part: the file part of the query, may be None
###
### @return list or raises likely KeyError from missing expected fields
def _ParseSDLResponse(response, accession: str, file_part: str):
    """ Parse SDL Response JSON """
    version = response.get('version')
    if version and version == '2':
        return list(_ParseSDLResponseV2(response, accession, file_part))

    msg = response.get('message')
    return list({'status': str(response['status']), 'msg': msg if msg else response.get('msg')})

def _MD5_SDLResponses(response):
    m = hashlib.md5()
    for digest in sorted(x['md5'].encode('ascii') for x in response):
        m.update(digest)
    return m.hexdigest()

def _Split_SRA_ID(object_id: str):
    """ Match SRA accession pattern and split into (useful?) components """
    m = re.match(r'^([EDS])R([APRSXZ])(\d{6,9})(?:\.(.+)){0,1}', object_id)
    if m:
        (issuer, type, serialNo, remainder) = m.groups()
        return (issuer, type, serialNo, remainder)
    return (None, None, None, None)

def _GetObject(object_id: str, expand: bool, requestURL: str):
    (issuer, type, serialNo, file_part) = _Split_SRA_ID(object_id)
    if not issuer:
        return { 'status_code': 404, 'msg': "Only SRA accessions are available" }, 404

    accession = f"{issuer}R{type}{serialNo}"

    if type != 'R':
        return { 'status_code': 501, 'msg': "Only run accessions are implemented" }, 500

    ret = {
        "id": object_id,
        "self_uri": requestURL,  ###< this might not be right
    }

    params = {'accept-proto': 'https'}
    params['acc'] = accession

    hdrs = {}
    cet = GetCE()
    if cet:
        hdrs['ident'] = cet

    # MARK: THIS IS TEST CODE
    if issuer == 'S' and serialNo == '000000': # SRR000000 was never used
        test_response = """
{
    "version": "2",
    "result": [
        {
            "bundle": "SRR000000",
            "status": 200,
            "msg": "ok",
            "files": [
                {
                    "object": "remote|SRR000000",
                    "type": "bam/gzip",
                    "name": "f4.f.mscs.DMSO5.meth.merged.sorted.uniq.bam",
                    "size": 2299145289,
                    "md5": "aa8fbf47c010ee82e783f52f9e7a21d0",
                    "modificationDate": "2019-08-30T15:21:11Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR000000/f4.f.mscs.DMSO5.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR000000",
                    "type": "bam/gzip",
                    "name": "f4.m.liv.DMSO1.rna.merged.sorted.bam",
                    "size": 1128363105,
                    "md5": "02b1ea5174fee52d14195fd07ece176a",
                    "modificationDate": "2019-08-30T15:04:29Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR000000/f4.m.liv.DMSO1.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                }
            ]
        }
    ]
}
        """
        ret['sdl_status'] = 200
        ret['sdl_json'] = test_response
        res = _ParseSDLResponse(json.loads(test_response), accession, file_part)
    else:
        sdl = requests.post(SDL_RETRIEVE_CGI, data=params, headers=hdrs)
        ret['sdl_status'] = sdl.status_code
        ret['sdl_json'] = sdl.json()

        try:
            res = _ParseSDLResponse(sdl.json(), accession, file_part)
        except:
            logging.error("unexpected response from SDL: " + sdl.text)
            return { 'status_code': 500, 'msg': 'Internal server error' }, 500

    if len(res) == 0:
        return { 'status_code': 404, 'msg': 'not found' }, 404

    if file_part:
        if len(res) != 1 or res[0]['id'] != object_id or not res[0]['access_methods'] or len(res[0]['access_methods']) == 0:
            logging.error("unexpected response from SDL: " + sdl.text)
            return { 'status_code': 500, 'msg': 'Internal server error' }, 500
        res = res[0]
        if res['status'] != '200':
            return { 'status_code': res['status'], 'msg': res['msg'] }, res['status']

        ret.update({
                'name': res['name'],
                'size': res['size'],
                'checksums': [{'checksum': res['md5'], 'type': 'md5'}],
                'created_time': res['date'],
                'access_methods': res['access_methods']
            })
        return ret
    else:
        if res[0]['status'] != '200':
            return { 'status_code': res[0]['status'], 'msg': res[0]['msg'] }, res[0]['status']

        ret.update({
            'checksums': [{'checksum': _MD5_SDLResponses(res), 'type': 'md5'}],
            'size': sum(x['size'] for x in res),
            'created_time': min(x['date'] for x in res),
            'contents': list({ 'id': x['id'], 'name': x['name'] } for x in res)
        })
        return ret

def GetObject(object_id: str, expand: bool):
    logging.info(f"In GetObject {object_id} {expand}")
    logging.info(f"params is {connexion.request.json}")
    logging.info(f"query is {connexion.request.args}")

    return _GetObject(object_id, expand, connexion.request.url)

def GetAccessURL(object_id: str, access_id: str):
    logging.info(f"In GetAccessURL {object_id} {access_id}")
    logging.info(f"params is {connexion.request.json}")
    logging.info(f"query is {connexion.request.args}")

    return {'status_code': 401, 'msg': "GetAccessURL is unused"}, 401  ###< this might not be right


# ------------- Computing Environment


def Base64(val):
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


def _GetAWS_CE():
    """ Get Compute Environment for AWS """
    try:  # AWS
        AWS_INSTANCE_URL = "http://169.254.169.254/latest/dynamic/instance-identity"

        document = requests.get(AWS_INSTANCE_URL + "/document")
        if document.status_code == requests.codes.ok:
            # encode the components
            doc_b64 = Base64(document.text)
            pkcs7 = requests.get(AWS_INSTANCE_URL + "/pkcs7")
            pkcs7_b64 = Base64(
                "-----BEGIN PKCS7-----\n" + pkcs7.text + "\n-----END PKCS7-----\n"
            )

            return doc_b64 + "." + pkcs7_b64
    except:
        pass

    return None


def _GetGCP_CE():
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


def GetCE():
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


# --------------------- Unit tests

_verbose = None

import test_values

class TestServer(unittest.TestCase):
    # TODO: Not very useful without rest of HTTP/Connexion framework

    def OnGCP(self):
        return _cloud == _GetGCP_CE

    def OnAWS(self):
        return _cloud == _GetAWS_CE

    # test cases

    def test_GetCE_docstring(self):
        # make sure has a docstring
        self.assertTrue(GetCE.__doc__)

    def test_GetCE(self):
        # output on the current platform
        s = GetCE()

        if self.OnGCP():
            # an instance identity token, base64url-encoded
            if _verbose:
                print("GCP detected")
            self.assertNotEqual(s, "")

        elif self.OnAWS():
            # a base64-encoded Instance Identity Document (Json) followed by "." and a base64-encoded pkcs7 signature
            if _verbose:
                print("AWS detected")
            self.assertNotEqual(s.find("."), -1)

        else:
            # neither AWS nor GCP: empty
            if _verbose:
                print("no cloud detected")
            self.assertEqual(s, None)

    def test_Request_for_run(self):
        res = _GetObject('SRR000000', 1, 'test') # expand doesn't matter, true and false should produce the same result
        self.assertEqual(res['size'], 2299145289+1128363105)
        self.assertEqual(res['created_time'], min('2019-08-30T15:21:11Z', '2019-08-30T15:04:29Z'))
        self.assertEqual(res['checksums'][0]['checksum'], hashlib.md5('02b1ea5174fee52d14195fd07ece176aaa8fbf47c010ee82e783f52f9e7a21d0'.encode('ascii')).hexdigest())
        self.assertIsInstance(res['contents'], list)
        self.assertEqual(len(res['contents']), 2)

    def test_Request_for_file(self):
        res = _GetObject('SRR000000.f4.m.liv.DMSO1.rna.merged.sorted.bam', 1, 'test')
        self.assertEqual(res['name'], 'f4.m.liv.DMSO1.rna.merged.sorted.bam')
        self.assertEqual(res['checksums'][0]['checksum'], '02b1ea5174fee52d14195fd07ece176a')

    def test_Request_for_run_and_file(self):
        res1 = _GetObject('SRR000000', 1, 'test')
        want = res1['contents'][0]
        res = _GetObject(want['id'], 1, 'test')
        self.assertEqual(res['id'], want['id'])
        self.assertEqual(res['name'], 'f4.f.mscs.DMSO5.meth.merged.sorted.uniq.bam')
        self.assertEqual(res['checksums'][0]['checksum'], 'aa8fbf47c010ee82e783f52f9e7a21d0')

def read():
    logging.info(f"In read()")
    return []


import sys

if __name__ == "__main__":
    _verbose = "--verbose" in sys.argv
    unittest.main()
