""" NCBI DRS server

    The entry points are GetObject, GetAccessURL, and PostAccessURL
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

import logging
from contextlib import contextmanager
from typing import Union

import connexion
from flask import make_response

CANONICAL_ROOT_URL = 'localhost'
SIGNED_URL_EXPIRATION = 10 * 60

logging.basicConfig(format="%(trans_id)s - %(message)s")


@contextmanager
def log_session():
    import uuid
    trans_id = uuid.uuid4().hex
    old_factory = logging.getLogRecordFactory()

    def new_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.trans_id = trans_id
        return record

    logging.setLogRecordFactory(new_factory)
    try:
        yield trans_id
    finally:
        logging.setLogRecordFactory(old_factory)


class DRS_Response:
    def __init__(self, obj: Union[dict, str] = None, code: int = None):
        if not obj and not code:
            self.data = {}
            self.status_code = 200
            return
        if isinstance(obj, str):
            if isinstance(code, int) and code != 200:
                self.data = dict(msg=obj)
                self.status_code = code
                return
            raise ValueError
        self.data = dict(obj)
        self.status_code = self.data.pop('status_code', 200)
        if isinstance(code, int):
            self.status_code = code
        return

    @property
    def is_good(self):
        return self.status_code == 200 and self.data

    @property
    def is_error(self):
        return self.status_code != 200

    def __repr__(self):
        return repr((self.status_code, self.data))

    def __str__(self):
        return str((self.status_code, self.data))

    def __getitem__(self, item):
        return self.data.__getitem__(item)

    def __contains__(self, item):
        return self.data.__contains__(item)

    def __getattr__(self, item):
        return self.data.get(item)

    @property
    def response(self):
        if self.status_code == 200:
            return make_response(self.data, 200)
        else:
            return make_response(dict(self.data, status_code=self.status_code),
                                 self.status_code)

    def log(self, function: str, object_id: str, *args):
        lhs = ' '.join([function, object_id] + [x for x in args if x])
        if self.status_code == 200:
            logging.info(f"{lhs} -> {self.data}")
        else:
            logging.warning(f"{lhs} !! {self.status_code} {self.data}")

    @staticmethod
    def standard_response(code: int):
        standard_responses = {
            401: "This data requires access permissions.",
            409: "The file has been moved offline.",
            410: "The file has been updated and the requested version is not available."
        }
        return DRS_Response({'msg': standard_responses[code]}, code)


class DRS_Request:
    def __init__(self, trans_id: str, object_id: str, expand: bool = False,
                 access_id: str = None, passport: str = None):
        self.reply_computed = None
        self.object_id = object_id
        self.expand = expand
        self.access_id = access_id
        self.passport = passport
        self.db_object = DRS_Request.call_db(self.object_id, self.expand)
        if self.passport:
            self.ras_clr = DRS_Request.call_ras(self.passport, trans_id)
        else:
            self.ras_clr = DRS_Response()

    @property
    def reply(self) -> DRS_Response:
        if self.reply_computed is None:
            self.reply_computed = self._compute_reply()

        return self.reply_computed

    def log(self, entry_point: str) -> None:
        self.reply.log(entry_point, self.object_id,
                       self.access_id, self.passport)

    def _compute_reply(self) -> DRS_Response:
        if self.ras_clr.is_error:
            return self.ras_clr
        if not self.db_object:
            return DRS_Response("DRS ID not found", 404)
        return self.__access_url if self.access_id else self.__object

    @property
    def __access_url(self) -> DRS_Response:
        """ Transforms the data object to a DRS AccessURL. """
        rslt = self.__good_locations
        if rslt.is_error:
            return rslt

        loc = rslt.good
        if loc.get('signing_account'):
            logging.info(f"signing url with {loc['signing_account']}")
            return DRS_Request.call_url_signer(loc)

        logging.debug("public data")
        return DRS_Response(dict(url=loc['file_name']))

    @property
    def __object(self) -> DRS_Response:
        """ Transforms the data object to a DRS DrsObject. """

        def contents_object(obj: dict) -> dict:
            """ Transforms the database version of the ContentsObject to the DRS version. """
            child = {
                'id': obj['childID'],
                'name': obj['childName'],
            }
            children = obj.get('children')
            if children:
                child['contents'] = [contents_object(x) for x in children]
            return child

        result = {
            'id': self.db_object['objectID'],
            'self_url': self.__url,
            'name': self.db_object['objectName'],
            'checksums': [{'type': 'md5', 'checksum': self.db_object['objectChecksum']}],
            'size': self.db_object['objectSize'],
            'created_time': self.db_object['objectCreateTime'].strftime('%Y-%m-%dT%H:%M:%SZ')
        }
        children = self.db_object.get('children')
        if children:
            result['contents'] = [contents_object(child) for child in children]
        elif self.db_object['locations']:
            rslt = self.__access_methods
            if rslt.is_error:
                return rslt
            result['access_methods'] = rslt.locations
        return DRS_Response(result)

    @property
    def __access_methods(self) -> DRS_Response:
        rslt = self.__good_locations
        if rslt.is_error:
            return rslt

        def access_method(loc) -> dict:
            """ Transforms a location into a DRS AccessMethod. """
            rslt = {
                'access_id': loc['access_id'],
                'type': "https"
            }
            rslt['provider'] = loc['bucketProvider']
            rslt['region'] = loc['bucketRegion']
            rslt['payment-required'] = True if loc['bucketIsUserPays'] else False
            return rslt

        return DRS_Response({'locations': [access_method(x) for x in rslt.good]})

    @property
    def __url(self) -> str:
        from urllib.parse import urlunsplit
        return urlunsplit(('drs', CANONICAL_ROOT_URL, self.db_object['objectID'], None, None))

    @property
    def __good_locations(self) -> DRS_Response:
        locations = self.db_object['locations']
        if locations:
            if not self.access_id:
                return DRS_Response(dict(good=locations))

            right_id = [x for x in locations if x['access_id'] == self.access_id]
            if right_id:
                return DRS_Response(dict(good=right_id[0]))
        logging.debug("file not found")
        return DRS_Response("File not found", 404)

    @staticmethod
    def call_db(object_id: str, expand: bool) -> dict:
        """ This function is a target for mocking """
        from .db import GetFullObject
        return GetFullObject(object_id, expand)

    @staticmethod
    def call_ras(passport: str, trans_id: str) -> DRS_Response:
        """ This function is a target for mocking """
        raise NotImplementedError

    @staticmethod
    def call_url_signer(loc) -> DRS_Response:
        """ This function is a target for mocking """
        raise NotImplementedError


def GetObject(object_id: str, expand: bool):
    """ Implements GET /objects/<object_id>

        This is an entry point.
    """
    with log_session() as trans_id:
        drs_request = DRS_Request(trans_id, object_id, expand)
        drs_request.log('GetObject')
        return drs_request.reply.response


def GetAccessURL(object_id: str, access_id: str):
    """ Implements GET /objects/<object_id>/access/<access_id>

        This is an entry point.
    """
    with log_session() as trans_id:
        drs_request = DRS_Request(trans_id, object_id, access_id=access_id)
        drs_request.log('GetAccessURL')
        return drs_request.reply.response


def PostAccessURL(object_id: str, access_id: str):
    """ Implements POST /objects/<object_id>/access/<access_id>

        POST method is an extension of the spec to
        accommodate for very long auth tokens.

        This is an entry point.
    """
    with log_session() as trans_id:
        drs_request = DRS_Request(trans_id, object_id, access_id=access_id,
                                  passport=connexion.request.json['ga4gh_passport'])
        drs_request.log('PostAccessURL')
        return drs_request.reply.response


def apikey_auth(token, required_scopes):
    logging.info(f"Got server apikey {token} {required_scopes}")
    ok = {"uid": 100}
    if False:
        raise connexion.OAuthProblem("Invalid token")
    return ok
