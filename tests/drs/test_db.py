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
from drs.db import GetFullObject


class Test_db(unittest.TestCase):
    def test1_GetFullObject(self):
        obj = GetFullObject('7d0b9ed4958e876a6a50ef6ae134de0f', True)
        self.assertIsNotNone(obj)
        self.assertIn('children', obj)
        self.assertEqual(len(obj['children']), 1)
        self.assertIn('objectID', obj['children'][0])
        self.assertEqual('dbf554827136113a58d0d1c32ca29e81', obj['children'][0]['objectID'])

    def test2_GetFullObject(self):
        obj = GetFullObject('dbf554827136113a58d0d1c32ca29e81', True)
        self.assertIsNotNone(obj)
        self.assertNotIn('children', obj)
        self.assertIn('locations', obj)
        self.assertGreater(len(obj['locations']), 0)
        self.assertIn('access_id', obj['locations'][0])


if __name__ == '__main__':
    logging.info("Starting unit tests")
    unittest.main(verbosity=5)
