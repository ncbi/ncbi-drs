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

def _ParseObjectId(objId: str):
    """ Split up an object id """
    type = None
    vers = None
    if objId:
        mtype = re.search(r'\.([^.]+)$', objId)
        if mtype:
            type = mtype[1]
            objId = objId[:-len(mtype[0])]
        mvers = re.search(r'\.(\d+)$', objId)
        if mvers:
            vers = mvers[1]
            objId = objId[:-len(mvers[0])]
        elif type and re.match(r'^\d+$', type):
            (type, vers) = (None, type)
    return (objId, vers, type)

### @brief _ParseSDLResponseV2 Parse version 2 SDL response JSON
###
### @param response: SDL response JSON
### @param query: { bundle: accession, type: file type }
###
### @return None if error else Dictionary with requested object or a 404
def _ParseSDLResponseV2(response, query):
    """ Parse version 2 SDL Response JSON """
    results = response.get('result')
    if type(results) != list:
        logging.error('unexpected result ' + results)
        return None

    for result in results:
        bundle = result.get('bundle')
        status = result.get('status')
        if not bundle or not status:
            return None

        status = str(status)
        if bundle == query['bundle']:
            if status != '200':
                return { 'status': status, 'msg': result.get('msg') }

            files = result.get('files')
            if type(files) != list:
                return None

            for file in files:
                filetype = file.get('type')
                if query['type'] in filetype:
                    locations = file.get('locations')
                    if type(locations) != list:
                        return None

                    for location in locations:
                        return {'status': '200'
                              , 'msg': result.get('msg')
                              , 'name': file.get('name')
                              , 'type': filetype
                              , 'size': file.get('size')
                              , 'md5': file.get('md5')
                              , 'date': file.get('modificationDate')
                              , 'url': location.get('link')
                              , 'service': location.get('service')
                              , 'region': location.get('region')
                              }

    return { 'status': '404', 'msg': 'not found' }

### @brief _ParseSDLResponse Parse SDL response JSON
###
### @param response: SDL response JSON
### @param query: { bundle: accession, type: file type }
###
### @return None if error else Dictionary
def _ParseSDLResponse(response, query):
    """ Parse SDL Response JSON """
    version = response.get('version')
    if version == '2':
        return _ParseSDLResponseV2(response, query)

    status = response.get('status')
    msg = response.get('message')
    if not msg: msg = response.get('msg')
    if status:
        return { 'status': str(status), 'msg': msg }

    return None

def _GetRedirURL(url: str, service: str, region: str):
    return url

def _GetAccessMethod(res):
    """ Create a DRS Access Method from SDL info """
    access_method = { 'access_url': _GetRedirURL(res['url'], res['service'], res['region']) }
    if res['service'] == 's3': access_method['type'] = 's3'
    elif res['service'] == 'gs': access_method['type'] = 'gs'
    else: access_method['type'] = 'https'
    if res['region']: access_method['region'] = res['region']
    return access_method

def _GetComputeEnvironmentToken():
    return GetCE()

def GetObject(object_id: str, expand: bool):
    logging.info(f"In GetObject {object_id} {expand}")
    logging.info(f"params is {connexion.request.json}")
    logging.info(f"query is {connexion.request.args}")

    ret = { 'id': object_id
          , 'self_uri': connexion.request.url ###< this might not be right
          }

    # ???: Confirm object_id matches [A-Za-z0-9.-_~]+
    (acc, vers, type) = _ParseObjectId('SRR10039049.bam') # _ParseObjectId(object_id)
    params = {'accept-proto': 'https'}
    params['acc'] = acc + '.' + vers if acc and vers else acc if acc else ''
    params['filetype'] = type if type else 'bam'

    hdrs = {}
    cet = _GetComputeEnvironmentToken()
    if cet: hdrs['ident'] = cet

    sdl = requests.post(SDL_RETRIEVE_CGI, data=params, headers=hdrs)
    ret["sdl_status"] = sdl.status_code
    ret["sdl_json"] = sdl.json()

    res = _ParseSDLResponse(sdl.json(), {'bundle': params['acc'], 'type': params['filetype']})
    if not res:
        logging.error('unexpected response ' + sdl.text)
    elif res['status'] == '200':
        # MARK: required fields
        ret['checksums'] = [{ 'checksum': res['md5'], 'type': 'md5' }]
        ret['size'] = res['size']
        ret['created_time'] = res['date']

        # MARK: optional fields
        if res['name']: ret['name'] = res['name']
        if vers: ret['version'] = vers

        # NOTE: this is were the URL is stored
        ret['access_methods'] = [ _GetAccessMethod(res) ]

    return ret

def GetAccessURL(object_id: str, access_id: str):
    logging.info(f"In GetAccessURL {object_id} {access_id}")
    logging.info(f"params is {connexion.request.json}")
    logging.info(f"query is {connexion.request.args}")

    return {'message': 'GetAccessURL is unused'}, 401 ###< this might not be right


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
            if _verbose: print('GCP detected')
            self.assertNotEqual(s, "")

        elif self.OnAWS():
            # a base64-encoded Instance Identity Document (Json) followed by "." and a base64-encoded pkcs7 signature
            if _verbose: print('AWS detected')
            self.assertNotEqual(s.find("."), -1)

        else:
            # neither AWS nor GCP: empty
            if _verbose: print('no cloud detected')
            self.assertEqual(s, None)

    def test_ParseObjectId_1(self):
        (base, vers, type) = _ParseObjectId('SRR000001')
        self.assertEqual(base, 'SRR000001')
        self.assertIsNone(vers)
        self.assertIsNone(type)

    def test_ParseObjectId_2(self):
        (base, vers, type) = _ParseObjectId('SRR000001.1.bam')
        self.assertEqual(base, 'SRR000001')
        self.assertEqual(vers, '1')
        self.assertEqual(type, 'bam')

    def test_ParseObjectId_3(self):
        (base, vers, type) = _ParseObjectId('SRR000001.1')
        self.assertEqual(base, 'SRR000001')
        self.assertEqual(vers, '1')
        self.assertIsNone(type)

    def test_ParseObjectId_4(self):
        (base, vers, type) = _ParseObjectId('SRR000001.bam')
        self.assertEqual(base, 'SRR000001')
        self.assertIsNone(vers)
        self.assertEqual(type, 'bam')

    def test_ParseSDLResponse_1(self):
        responseText = """
{
    "version": "2",
    "result": [
        {
            "bundle": "SRR10039049",
            "status": 200,
            "msg": "ok",
            "files": [
                {
                    "object": "remote|SRR10039049",
                    "type": "bam/gzip",
                    "name": "f4.f.mscs.DMSO5.meth.merged.sorted.uniq.bam",
                    "size": 2299145289,
                    "md5": "aa8fbf47c010ee82e783f52f9e7a21d0",
                    "modificationDate": "2019-08-30T15:21:11Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039049/f4.f.mscs.DMSO5.meth.merged.sorted.uniq.bam.1",
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
        res = _ParseSDLResponse(json.loads(responseText), { 'bundle': 'SRR10039049', 'type': 'bam'})
        self.assertIsNotNone(res)
        self.assertEqual(res['status'], '200')
        self.assertEqual(res['md5'], 'aa8fbf47c010ee82e783f52f9e7a21d0')
        self.assertIsNotNone(res.get('url'))
        self.assertEqual(res['name'], 'f4.f.mscs.DMSO5.meth.merged.sorted.uniq.bam')
        self.assertEqual(res['service'], 's3')

    def test_ParseSDLResponse_version(self):
        responseText = """
{
    "version": "unstable",
    "result": [
        {
            "bundle": "SRR10039049",
            "status": 200,
            "msg": "ok",
            "files": [
                {
                    "object": "remote|SRR10039049",
                    "type": "bam/gzip",
                    "name": "f4.f.mscs.DMSO5.meth.merged.sorted.uniq.bam",
                    "size": 2299145289,
                    "md5": "aa8fbf47c010ee82e783f52f9e7a21d0",
                    "modificationDate": "2019-08-30T15:21:11Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039049/f4.f.mscs.DMSO5.meth.merged.sorted.uniq.bam.1",
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
        res = _ParseSDLResponse(json.loads(responseText), { 'bundle': 'SRR10039049', 'type': 'bam'})
        self.assertIsNone(res)

    def test_ParseSDLResponse_404(self):
        responseText = """
{
    "version": "2",
    "result": [
        {
            "bundle": "SRR10039049",
            "status": 404,
            "msg": "Cannot resolve accession"
        }
    ]
}
"""
        res = _ParseSDLResponse(json.loads(responseText), { 'bundle': 'SRR10039049', 'type': 'bam'})
        self.assertIsNotNone(res)
        self.assertNotEqual(res['status'], '200')

    def test_ParseSDLResponse_not_found(self):
        responseText = """
{
    "version": "2",
    "result": [
        {
            "bundle": "SRR10039049",
            "status": 200,
            "msg": "ok",
            "files": [
                {
                    "object": "remote|SRR10039049",
                    "type": "bam/gzip",
                    "name": "f4.f.mscs.DMSO5.meth.merged.sorted.uniq.bam",
                    "size": 2299145289,
                    "md5": "aa8fbf47c010ee82e783f52f9e7a21d0",
                    "modificationDate": "2019-08-30T15:21:11Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039049/f4.f.mscs.DMSO5.meth.merged.sorted.uniq.bam.1",
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
        res = _ParseSDLResponse(json.loads(responseText), { 'bundle': 'foo', 'type': 'bam'})
        self.assertIsNotNone(res)
        self.assertEqual(res['status'], '404')

    def test_ParseSDLResponse_500(self):
        responseText = """{"status": 500, "message": "No accession to process"}"""
        res = _ParseSDLResponse(json.loads(responseText), { 'bundle': 'foo', 'type': 'bam'})
        self.assertIsNotNone(res)
        self.assertEqual(res['status'], '500')

    def test_ParseSDLResponse_empty(self):
        responseText = "{}"
        res = _ParseSDLResponse(json.loads(responseText), { 'bundle': 'foo', 'type': 'bam'})
        self.assertIsNone(res)


def read():
    logging.info(f"In read()")
    return []

import sys
if __name__ == "__main__":
    _verbose = ('--verbose' in sys.argv)
    unittest.main()
