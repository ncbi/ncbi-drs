""" Rewrite SDL URLs """

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

from tempfile import gettempdir
from datetime import datetime
from urllib.parse import urljoin
import json
import re
from secrets import token_urlsafe

def _timestamp() -> str:
    return datetime.utcnow().isoformat("T") + "Z"

_dir = gettempdir()
def _filepath(shortID: str) -> str:
    return f"{_dir}/gov.nih.nlm.ncbi.drs.{shortID}.tempurl"

class Rewriter:
    """ Rewrite SDL URL for our proxy
    """
    def Rewrite(self, urlString: str) -> str:
        """ Rewrite SDL URL for our proxy """
        for _ in range(5):
            shortID = token_urlsafe()
            try:
                with open(_filepath(shortID), 'x') as f:
                    json.dump({'from': urlString, 'to': shortID, 'when': _timestamp()}, f)
                    return shortID
            except FileExistsError:
                pass
        raise "something is wrong with secrets"

    def Retrieve(self, shortID: str) -> str:
        """ Extract original SDL URL from rewritten URL """
        try:
            with open(_filepath(shortID), 'r') as fh:
                obj = json.load(fh)
                # print(obj)
                return obj['from'] if obj['to'] == shortID else None
        except:
            return None

if __name__ == "__main__":
    r = Rewriter()
    n = r.Rewrite('foo')
    u = r.Retrieve(n)
    print(f"foo -> {n} -> {u}")

