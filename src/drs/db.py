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

__all__ = ['GetFullObject']

import os
import logging
import sqlite3
import hashlib
from datetime import datetime

cnx = sqlite3.connect(os.environ['DRS_DB'])


def convertToDateTime(value: str) -> datetime:
    try:
        return datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')
    except ValueError:
        return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')


def _get_object_contents(objID: int):
    """ Get all the child objects of an object """
    TABLES = " JOIN ".join([  'Containers'
                            , 'Objects O ON O.ROWID = contChild'])
    FIELDS = ['contChild', 'objectID', 'objectName']
    curs = cnx.cursor()
    for row in curs.execute(f"SELECT {', '.join(FIELDS)} FROM {TABLES} WHERE contParent = ?", (objID,)):
        yield { 'OID': row[0], 'objectID': row[1], 'objectName': row[2] }


def get_object_contents(objID: int, expand: bool) -> list:
    """ Get all the child objects of an object, possibly recursively """
    result = list(_get_object_contents(objID))
    if expand:
        for obj in result:
            children = get_object_contents(obj['OID'], expand)
            if children:
                obj['children'] = children
    for obj in result:
        del obj['OID']
    return result


def get_object(drsID: str) -> dict:
    """ Get object by its DRS ID """
    FIELDS = ['ROWID', 'objectCreateTime', 'objectSize', 'objectFileID', 'objectName']
    for row in cnx.execute(f"SELECT {', '.join(FIELDS)} FROM Objects WHERE objectID = ?", (drsID,)):
        return {
            'OID': row[0],
            'objectID': drsID,
            'objectCreateTime': convertToDateTime(row[1]),
            'objectSize': row[2],
            'objectFileID': row[3],
            'objectName': row[4],
        }
    return {}


def _get_location_info(fileID: int):
    """ Get all the locations for a file """
    TABLES = " JOIN ".join([  'FileLocations'
                            , 'Files ON fileID = flFileID'
                            , 'Buckets ON bucketID = flBucket'
                            , 'FileStates FS ON FS.ROWID = fileState'
                            , 'FileStates LS ON LS.ROWID = flState'
                            , 'FilePermissions P ON P.ROWID = filePermission'
                           ])
    FIELDS = [  'fileName'
              , 'fileMD5'
              , 'fileSize'
              , 'fileDate'
              , 'flURL'
              , 'bucketProvider'
              , 'bucketRegion'
              , 'bucketSigningAccount'
              , 'bucketIsUserPays'
              , 'coalesce(LS.stateName, FS.stateName) AS status'
              , 'permName']
    curs = cnx.cursor()
    for row in curs.execute(f"SELECT {', '.join(FIELDS)} FROM {TABLES} WHERE flFileID = ?", (fileID,)):
        result = dict(zip(FIELDS, row))
        result['status'] = result.pop(FIELDS[9])
        result['fileDate'] = convertToDateTime(result['fileDate'])
        if result['flURL'].startswith('https://') and result['status'] == 'online':
            result['access_id'] = hashlib.sha256(result['flURL'].encode()).hexdigest()
        yield result


def get_location_info(fileID: int) -> list:
    return list(_get_location_info(fileID))


def GetFullObject(drsID: str, expand: bool = False) -> dict:
    obj = get_object(drsID)
    if not obj:
        return {}
    children = get_object_contents(obj['OID'], expand)
    del obj['OID']
    if children:
        obj['children'] = children
    if obj['objectFileID']:
        obj['locations'] = get_location_info(obj['objectFileID'])
    del obj['objectFileID']
    logging.debug(obj)
    return obj


def add_access_id(loc: dict) -> dict:
    """ this is mostly an implementation detail but it gets used by testing
        because testing should not need to know the details of how to prepare
        test inputs that come from the database.
    """
    try:
        url = loc['flURL']
        if url.startswith('https://'):  # only https for now
            return dict(loc, access_id=hashlib.sha256(url.encode()).hexdigest())
    except KeyError:
        pass
    return loc
