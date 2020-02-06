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

from tempfile import mkstemp, gettempdir
import json
import datetime
import os
import re
from urllib.parse import urljoin

_dir = gettempdir()

class Rewriter:
    """ Rewrite SDL URL for our proxy
    """
    def rewrite(self, urlString: str, baseURL: str):
        """ Rewrite SDL URL for our proxy """
        (f, n) = mkstemp('.tempurl', 'gov.nih.nlm.ncbi.sra.drs.', _dir, True)
        m = re.search(r'gov\.nih\.nlm\.ncbi\.sra\.drs\.(.+)', n)
        r = m[1][:-8]
        fd = os.fdopen(f, mode='w')
        json.dump({'from': urlString, 'to': r, 'when': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')}, fd)
        fd.close()
        return urljoin(baseURL, r)

    def retrieve(self, urlString: str):
        """ Extract original SDL URL from rewritten URL """
        j = json.load(open(f"{_dir}/gov.nih.nlm.ncbi.sra.drs.{urlString}.tempurl"))
        # print(j)
        return j['from'] if j['to'] == urlString else None

if __name__ == "__main__":
    r = Rewriter()
    n = r.rewrite('foo', '')
    u = r.retrieve(n)
    print(u)

