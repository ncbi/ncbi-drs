""" SDL -> DRS bridging server

    The normal entry point is GetObject
"""

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
import json
import hashlib
from urllib.parse import urlsplit, urlunsplit, urljoin, urlencode
import sys
import os

try:
    from .rewrite import Rewriter
    from .cloud import ComputeEnvironmentToken
    from .token_extract import TokenExtractor
except:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from rewrite import Rewriter
    from cloud import ComputeEnvironmentToken
    from token_extract import TokenExtractor

# from connexion import NoContent
from flask import make_response, abort

SDL_RETRIEVE_CGI = "https://locate.ncbi.nlm.nih.gov/sdl/2/retrieve"
SDL_LOCALITY_CGI = "https://locate.ncbi.nlm.nih.gov/sdl/2/locality"

def apikey_auth(token, required_scopes):
    logging.info(f"Got server apikey {token} {required_scopes}")
    ok = {"uid": 100}
    if False:
        raise OAuthProblem("Invalid token")
    return ok

_rewriter = Rewriter()
_extractor = TokenExtractor()
_SDL_Redirector_Prefix = 'https://locate.ncbi.nlm.nih.gov/sdlr/sdlr.fcgi'

def _GetTestResponse() -> dict:
    return json.loads("""
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
                },
                {
                    "object": "remote|SRR000000",
                    "type": "sra",
                    "name": "SRR000000",
                    "size": 1128363105,
                    "md5": "02b1ea5174fee52d14195fd07ece176a",
                    "modificationDate": "2019-08-30T15:04:29Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR000000/SRR000000.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                }
            ]
        }
    ]
}
    """)

def _GetRedirURL(location, proxyURL: str) -> str:
    link = location['link']
    if link.startswith(_SDL_Redirector_Prefix):
        shortID = _rewriter.Rewrite(link)
        return urljoin(proxyURL, shortID)
    else:
        return link

def _TranslateService(location) -> str:
    try: return { 's3': 's3', 'gs': 'gs' }[location['service']]
    except: return 'https'

def _MakeAccessMethod(location, proxyURL: str) -> dict:
    """ Create a DRS Access Method from SDL info """
    access_method = { 'access_url': _GetRedirURL(location, proxyURL), 'type': _TranslateService(location) }
    if location.get('region'):
        access_method['region'] = location.get('region')
    return access_method

### @brief _ParseSDLResponseV2 Parse version 2 SDL response JSON
###
### @param response: SDL response JSON
### @param query: { bundle: accession, type: file type }
###
### @return nothing; it's a generator
def _ParseSDLResponseV2(response, accession: str, file_part: str, proxyURL: str) -> None:
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
                access_methods = list(_MakeAccessMethod(location, proxyURL) for location in file['locations'])

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
def _ParseSDLResponse(response, accession: str, file_part: str, proxyURL: str) -> list:
    """ Parse SDL Response JSON """
    version = response.get('version')
    if version and version == '2':
        return list(_ParseSDLResponseV2(response, accession, file_part, proxyURL))

    msg = response.get('message')
    return [{'status': str(response['status']), 'msg': msg if msg else response.get('msg')}]

def _MD5_SDLResponses(response: dict) -> str:
    """ See: https://ga4gh.github.io/data-repository-service-schemas/preview/release/drs-1.0.0/docs/#_drsobject

        checksums field
    """
    m = hashlib.md5()
    for digest in sorted(x['md5'].encode('ascii') for x in response):
        m.update(digest)
    return m.hexdigest()

def _Split_SRA_ID(object_id: str) -> (str, str, str, str):
    """ Match SRA accession pattern and split into (useful?) components """
    m = re.match(r'^([EDS])R([APRSXZ])(\d{6,9})(?:\.(.+)){0,1}$', object_id)
    if m:
        (issuer, type, serialNo, remainder) = m.groups()
        return (issuer, type, serialNo, remainder)
    return (None, None, None, None)

def _drsURI(requestURL: str, objectID: str) -> str:
    """ See: https://ga4gh.github.io/data-repository-service-schemas/preview/release/drs-1.0.0/docs/#_drs_uris """
    (scheme, netloc, *dummy) = urlsplit(requestURL)
    return urlunsplit(('drs', netloc, objectID, None, None))

def _ProcessSDLResponseWithFilePart(res: dict, object_id: str) -> dict:
    if res['id'] == object_id:
        if res['status'] == '200':
            return {
                'name': res['name'],
                'size': res['size'],
                'checksums': [{'checksum': res['md5'], 'type': 'md5'}],
                'created_time': res['date'],
                'access_methods': res['access_methods']
            }
        return { 'status_code': res['status'], 'msg': res['msg'] }
    raise "unexpected"

def _ProcessSDLResponse(sdlResponse: dict, object_id: str, accession: str, file_part: str, proxyURL: str) -> dict:
    res = _ParseSDLResponse(sdlResponse, accession, file_part, proxyURL)

    if not res:
        return { 'status_code': 404, 'msg': 'not found' }

    if file_part:
        return _ProcessSDLResponseWithFilePart(res[0], object_id)

    if res[0]['status'] == '200':
        return {
            'checksums': [{'checksum': _MD5_SDLResponses(res), 'type': 'md5'}],
            'size': sum(x['size'] for x in res),
            'created_time': min(x['date'] for x in res),
            'contents': list({ 'id': x['id'], 'name': x['name'] } for x in res)
        }
    return { 'status_code': res[0]['status'], 'msg': res[0]['msg'] }

def _GetObject(object_id: str, expand: bool, requestURL: str, requestHeaders: dict = {}) -> dict:
    """ Internal testable implementataion of the GET /objects/<object_id>

        This is the main function.
    """
    (scheme, netloc, *dummy) = urlsplit(requestURL)
    proxyURL = urlunsplit((scheme, netloc, 'proxy/', None, None))

    (issuer, type, serialNo, file_part) = _Split_SRA_ID(object_id)
    if not issuer:
        return { 'status_code': 404, 'msg': "Only SRA accessions are available" }, 404, {}

    accession = f"{issuer}R{type}{serialNo}"

    if type != 'R':
        return { 'status_code': 501, 'msg': "Only run accessions are implemented" }, 501, {}

    ret = {
        "id": object_id,
        "self_uri": _drsURI(requestURL, object_id)
    }

    #params = {'accept-proto': 'https'}
    #params['acc'] = accession

    params = {'acc': accession}

    post_body = {}
    auth = _extractor.extract(requestHeaders.get('Authorization'))
    if auth:
        post_body['cart'] = auth

    cet = ComputeEnvironmentToken()
    if cet:
        post_body['location'] = cet

    sdl_json = None
    sdl_text = None
    sdl_status = None

    if issuer == 'S' and serialNo == '000000': # SRR000000 was never used
        # MARK: THIS IS TEST CODE
        sdl_json = _GetTestResponse()
        sdl_text = json.dumps(sdl_json)
        sdl_status = 200
    else:
        url = SDL_RETRIEVE_CGI + '?' + urlencode(params)
        ret['_debug_request_url'] = url
        ret['_debug_form_body'] = post_body
        try:
            sdl = requests.post(url, data=post_body)
        except:
            logging.error("failed to contact SDL")
            ret.update({ 'status_code': 500, 'msg': 'Internal server error' })
            return ret, 500, {}
        else:
            sdl_json = sdl.json()
            sdl_text = sdl.text
            sdl_status = sdl.status_code

    ret['_debug_sdl_status'] = sdl_status
    ret['_debug_sdl_text'] = sdl_text
    if sdl_status != 200:
        logging.error(f"unexpected response from SDL: {sdl_status}")
        ret.update({ 'status_code': 500, 'msg': f"Internal server error: SDL returned {sdl_status}" })
        return ret, 500, {}

    try:
        res = _ProcessSDLResponse(sdl_json, object_id, accession, file_part, proxyURL)
    except:
        logging.error("unexpected response from SDL: " + json.dumps(sdl_json))
        ret.update({ 'status_code': 500, 'msg': 'Internal server error' })
        return ret, 500, {}

    if 'status_code' not in res:
        ret.update(res)
        return ret, 200, {}

    return ret, res['status_code'], {}

def GetObject(object_id: str, expand: bool):
    """ Implements the GET /objects/<object_id>

        See: https://ga4gh.github.io/data-repository-service-schemas/preview/release/drs-1.0.0/docs/#_getaccessurl

        This is the main entry point.
    """
    logging.info(f"In GetObject {object_id} {expand}")
    logging.info(f"params is {connexion.request.json}")
    logging.info(f"query is {connexion.request.args}")

    return _GetObject(object_id, expand, connexion.request.url, connexion.request.headers)

def GetAccessURL(object_id: str, access_id: str):
    """ Implements the GET /objects/<object_id>/access/<access_id>

        See: https://ga4gh.github.io/data-repository-service-schemas/preview/release/drs-1.0.0/docs/#_getaccessurl

        This is unused by us.
    """
    logging.info(f"In GetAccessURL {object_id} {access_id}")
    logging.info(f"params is {connexion.request.json}")
    logging.info(f"query is {connexion.request.args}")

    return {'status_code': 401, 'msg': "GetAccessURL is unused"}


# --------------------- Unit tests

class _TestServer(unittest.TestCase):
    def test_Split_SRA_ID_S(self):
        (issuer, type, serialNo, file_part) = _Split_SRA_ID('SRR000000')
        self.assertEqual(issuer, 'S')
        self.assertEqual(type, 'R')
        self.assertEqual(serialNo, '000000')
        self.assertFalse(file_part)

    def test_Split_SRA_ID_E(self):
        (issuer, type, serialNo, file_part) = _Split_SRA_ID('ERR000000')
        self.assertEqual(issuer, 'E')
        self.assertEqual(type, 'R')
        self.assertEqual(serialNo, '000000')
        self.assertFalse(file_part)

    def test_Split_SRA_ID_D(self):
        (issuer, type, serialNo, file_part) = _Split_SRA_ID('DRR000000')
        self.assertEqual(issuer, 'D')
        self.assertEqual(type, 'R')
        self.assertEqual(serialNo, '000000')
        self.assertFalse(file_part)

    def test_Split_SRA_ID_file_part(self):
        (issuer, type, serialNo, file_part) = _Split_SRA_ID('SRR000000.f4.m.liv.DMSO1.rna.merged.sorted.bam')
        self.assertEqual(issuer, 'S')
        self.assertEqual(type, 'R')
        self.assertEqual(serialNo, '000000')
        self.assertEqual(file_part, 'f4.m.liv.DMSO1.rna.merged.sorted.bam')

    def test_Split_SRA_ID_X(self):
        (issuer, type, serialNo, file_part) = _Split_SRA_ID('XRR000000')
        self.assertFalse(issuer)
        self.assertFalse(type)
        self.assertFalse(serialNo)
        self.assertFalse(file_part)

    def test_Split_SRA_ID_Fail_1(self):
        (issuer, type, serialNo, file_part) = _Split_SRA_ID('SRR000000-a')
        self.assertFalse(issuer)
        self.assertFalse(type)
        self.assertFalse(serialNo)
        self.assertFalse(file_part)

    def test_Split_SRA_ID_Fail_2(self):
        (issuer, type, serialNo, file_part) = _Split_SRA_ID('SRY000000')
        self.assertFalse(issuer)
        self.assertFalse(type)
        self.assertFalse(serialNo)
        self.assertFalse(file_part)

    def test_drsURI(self):
        uri = _drsURI('http://localhost:8080/ga4gh/drs/v1/objects/SRR000000', 'SRR000000')
        self.assertEqual(uri, 'drs://localhost:8080/SRR000000')

    def test_Request_for_run(self):
        res = _ProcessSDLResponse(_GetTestResponse(), 'SRR000000', 'SRR000000', None, 'http://localhost:8080/proxy')
        self.assertEqual(res['size'], 2299145289+1128363105+1128363105)
        self.assertEqual(res['created_time'], min('2019-08-30T15:21:11Z', '2019-08-30T15:04:29Z'))
        self.assertEqual(res['checksums'][0]['checksum'], hashlib.md5('02b1ea5174fee52d14195fd07ece176a02b1ea5174fee52d14195fd07ece176aaa8fbf47c010ee82e783f52f9e7a21d0'.encode('ascii')).hexdigest())
        self.assertIsInstance(res['contents'], list)
        self.assertEqual(len(res['contents']), 3)

    def test_Request_for_file(self):
        res = _ProcessSDLResponse(_GetTestResponse(), 'SRR000000.f4.m.liv.DMSO1.rna.merged.sorted.bam', 'SRR000000', 'f4.m.liv.DMSO1.rna.merged.sorted.bam', 'http://localhost:8080/proxy')
        self.assertEqual(res['checksums'][0]['checksum'], '02b1ea5174fee52d14195fd07ece176a')
        self.assertIsNotNone(res['access_methods'][0]['access_url'])

    def test_GetObject(self):
        (res1, *dummy) = _GetObject('SRR000000', True, 'http://localhost:8080/ga4gh/drs/v1/objects/SRR000000')
        want = res1['contents'][0]
        (res, *dummy) = _GetObject(want['id'], True, 'http://localhost:8080/ga4gh/drs/v1/objects/'+want['id'])
        self.assertEqual(res['id'], want['id'])
        self.assertEqual(res['name'], 'f4.f.mscs.DMSO5.meth.merged.sorted.uniq.bam')
        self.assertEqual(res['checksums'][0]['checksum'], 'aa8fbf47c010ee82e783f52f9e7a21d0')
        self.assertIsNotNone(res['access_methods'][0]['access_url'])
        # print(res['access_methods'][0]['access_url'])

if __name__ == "__main__":
    unittest.main()
