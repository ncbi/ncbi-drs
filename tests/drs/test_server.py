#!/usr/bin/env python3
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
#
# flake8: noqa
# NO QA ON TESTING CODE

import logging
import unittest
import secrets
from unittest.mock import patch
from drs.server import DRS_Request, DRS_Response


class Test_DRS_Request(unittest.TestCase):
    """ Mock up the 3 outbound function of DRS_Request
        call_db, call_ras, call_url_signer. With these
        3 functions mocked, DRS_Request requires nothing
        outside of itself. It requires no configuration
        and no database.

        Use the mocks to drive DRS_Request and test
        that the reply object it produces contains
        the expected values.
    """
    @patch('drs.server.DRS_Request.call_url_signer')
    @patch('drs.server.DRS_Request.call_ras')
    @patch('drs.server.DRS_Request.call_db')
    def test_404(self, call_db, call_ras, call_signer):
        """ normal response for unknown DRS ID """
        call_db.return_value = {}

        obj = DRS_Request('test', 'foo')
        self.assertGoodError(obj.reply, 404)
        self.assertFalse(call_ras.called)
        self.assertFalse(call_signer.called)

    @patch('drs.server.DRS_Request.call_url_signer')
    @patch('drs.server.DRS_Request.call_ras')
    @patch('drs.server.DRS_Request.call_db')
    def test_get_object_okay_1(self, call_db, call_ras, call_signer):
        """ normal good response """
        call_db.return_value = self.db_result('3d647f9d5d29e7913cde82774d79658a')

        obj = DRS_Request('test', '3d647f9d5d29e7913cde82774d79658a')
        self.assertGoodBundleObject(obj.reply, '3d647f9d5d29e7913cde82774d79658a', 2)
        self.assertFalse(call_ras.called)
        self.assertFalse(call_signer.called)

    @patch('drs.server.DRS_Request.call_url_signer')
    @patch('drs.server.DRS_Request.call_ras')
    @patch('drs.server.DRS_Request.call_db')
    def test_get_object_okay_2(self, call_db, call_ras, call_signer):
        """ normal good response """
        call_db.return_value = self.db_result('7d0b9ed4958e876a6a50ef6ae134de0f')

        obj = DRS_Request('test', '7d0b9ed4958e876a6a50ef6ae134de0f')
        self.assertGoodBundleObject(obj.reply, '7d0b9ed4958e876a6a50ef6ae134de0f', 1)
        self.assertFalse(call_ras.called)
        self.assertFalse(call_signer.called)

    @patch('drs.server.DRS_Request.call_url_signer')
    @patch('drs.server.DRS_Request.call_ras')
    @patch('drs.server.DRS_Request.call_db')
    def test_access_1(self, call_db, call_ras, call_signer):
        """ normal good response """
        call_db.return_value = self.db_result('dbf554827136113a58d0d1c32ca29e81')

        obj = DRS_Request('test', 'dbf554827136113a58d0d1c32ca29e81'
                          , access_id='325a10e68ac4c3d77e190ecde2296585c6f1a98d4c4675524b9bc2803e1af4f9')
        self.assertGoodAccessUrl(obj.reply)
        self.assertFalse(call_ras.called)
        self.assertFalse(call_signer.called)

    def assertGoodError(self, reply, status_code):
        self.assertEqual(reply.status_code, status_code)
        self.assertIn('msg', reply)
        self.assertTrue(reply['msg'])

    def assertGoodChecksum(self, checksum, object_id):
        self.assertIn('type', checksum)
        self.assertIn('checksum', checksum)
        self.assertEqual(checksum['type'], 'md5')
        self.assertEqual(checksum['checksum'], object_id)

    def assertGoodObject(self, reply, object_id):
        self.assertTrue(reply.is_good)
        for key in ['checksums', 'created_time', 'id', 'self_url', 'size', ]:
            self.assertIn(key, reply)
        self.assertEqual(reply['id'], object_id)
        self.assertEqual(len(reply['checksums']), 1)
        self.assertGoodChecksum(reply['checksums'][0], object_id)

    def assertGoodBundleObject(self, reply, object_id, count):
        self.assertGoodObject(reply, object_id)
        self.assertIn('contents', reply)
        self.assertNotIn('access_methods', reply)
        self.assertEqual(len(reply['contents']), count)

    def assertGoodFileObject(self, reply, object_id, count):
        self.assertGoodObject(reply, object_id)
        self.assertIn('access_methods', reply)
        self.assertNotIn('contents', reply)
        self.assertEqual(len(reply['access_methods']), count)

    def assertGoodAccessUrl(self, reply):
        self.assertTrue(reply.is_good)
        self.assertIn('url', reply)
        self.assertTrue(reply['url'])

    def db_result(self, object_id):
        from copy import deepcopy
        return deepcopy(Test_DRS_Request._call_db_test_values[object_id])

    def ras_result(self, user_id):
        return Test_DRS_Request._call_ras_test_values[user_id]

    _call_db_test_values = {}  # indexed by objectID
    _call_ras_test_values = {}  # indexed by user-id

    @classmethod
    def setUpClass(cls):
        from pathlib import Path
        import json
        from datetime import datetime

        super().setUpClass()
        logging.info("Loading canned responses...")
        with open(Path(__file__).parent.joinpath('db-responses.json')) as f:
            for obj in json.load(f):
                obj['objectCreateTime'] = datetime.strptime(obj['objectCreateTime'], '%Y-%m-%d %H:%M:%S.%f')
                try:
                    # noinspection PyProtectedMember
                    from drs.db import add_access_id
                    x = [add_access_id(x) for x in obj['locations']]
                    obj['locations'] = x
                except KeyError:
                    pass
                cls._call_db_test_values[obj['objectID']] = obj
        logging.info(f"Loaded {len(cls._call_db_test_values.keys())} DRS data canned responses.")
        try:
            with open(Path(__file__).parent.joinpath('CLR-responses.json')) as f:
                for obj in json.load(f):
                    cls._call_ras_test_values[obj['user-id']] = DRS_Response(dict(consents=obj['dbgap-consents']))
        except FileNotFoundError:
            cls._call_ras_test_values = {}
        logging.info(f"Loaded {len(cls._call_ras_test_values.keys())} RAS Clearinghouse canned responses.")


if __name__ == '__main__':
    logging.info("Starting unit tests")
    unittest.main(verbosity=5)
