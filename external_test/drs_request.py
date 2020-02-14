#!/usr/bin/env python

import sys, base64, json
import urllib.parse as parse
import http.client as client
import hashlib
from timeit import default_timer as timer

def file_2_string( filename : str ) -> str :
    res = None
    with open( filename, 'r' ) as f :
        res = f.read().replace( '\n', '' ).strip()
    return res

def str_to_int( s : str, dflt : int = 0 ) -> int :
    try:
        return int( s )
    except ValueError :
        return dflt

def continue_or_cancel() -> int :
    print( "[ 1 ] ... continue" )
    print( "[ 2 ] ... cancel" )
    return str_to_int( input( "your choice: " ) )

def requesting( accession : str, cart : str, drs_url : str ) -> ( int, str ):
    status = None
    res = ""
    url = "{}{}".format( drs_url, accession )
    url_parts = parse.urlparse( url )
    conn = client.HTTPConnection( url_parts.netloc )
    headers = { "Authorization" : "Bearer {}".format( cart ) }
    conn.request( "GET", url_parts.path, "", headers )
    resp = conn.getresponse()
    status = resp.status
    print( "status : {}".format( status ) )
    while True:
        chunk = resp.read( 1024 * 1024 )
        if len( chunk ) :
            res = res + chunk.decode( "utf-8" )
        else :
            break
    conn.close()
    return ( status, res )

def select_item( items ) :
    res = ""
    num = 1
    for item in items :
        print( "[ {} ] ... {}".format( num, item[ 'id' ] ) )
        num = num + 1
    print( "[ {} ] ... cancel".format( num ) )
    selection = str_to_int( input( "your choice: " ) )
    if selection > 0 and selection < len( items ) :
        res = items[ selection - 1 ][ 'id' ]
    return res

def read_loop( url : str, chunk_size : int )  -> ( int, str, float ) :
    num_read : int = 0
    hash : str = ""
    elapsed : float = 0.0

    url_parts = parse.urlparse( url )
    conn = client.HTTPConnection( url_parts.netloc )
    conn.request( "GET", url_parts.path )
    resp = conn.getresponse()
    status = resp.status
    print( "connected - status: {}".format( status ) )
    if status == 200 :
        hasher = hashlib.md5()
        start = timer()
        while True :
            chunk = resp.read( chunk_size )
            if len( chunk ) :
                hasher.update( chunk )
                num_read = num_read + len( chunk )
                sys.stdout.write( '.' )
                sys.stdout.flush()
            else :
                hash = hasher.hexdigest()
                break
        end = timer()
        elapsed = end - start

    conn.close()
    return ( num_read, hash, elapsed )

def try_parse_json( s ) :
    res = None
    try :
        res = json.loads( s )
    except :
        pass
    return res

#===================================================================================
if __name__ == '__main__':

    print( "running: '{}'".format( __file__ ) )

    if sys.version_info[ 0 ] < 3 :
        print( "does not work with python version < 3!" )
        sys.exit( 3 )

    nargs = len( sys.argv )
    if nargs < 4 :
        print( "please specify an accession and a drs-domain/ip-address and a cart-file" )
        print( "python drs_request SRRXXXXXX http://YYY.YYY.YYY.YYY cart.txt" )
        sys.exit( 3 )

    accession = sys.argv[ 1 ]
    print( "requesting: {}".format( accession ) )
    drs_domain = sys.argv[ 2 ]
    print( "from : {}".format( drs_domain ) )
    cartfilename = sys.argv[ 3 ]
    print( "using cart : '{}'\n".format( cartfilename ) )
    
    cart = file_2_string( cartfilename )
    if cart == None :
        print( "\cannot read cartfile:\n{}".format( cartfilename ) )
        sys.exit( 3 )

    drs_url = "{}/ga4gh/drs/v1/objects/".format( drs_domain )
    ( status1, reply1 ) = requesting( accession, cart, drs_url )
    if status1 == None :
        print( "1st request to {} failed.".format( drs_url ) )
        sys.exit( 3 )

    if status1 != 200 :
        print( reply1 )
        sys.exit( 3 )

    parsed1 = try_parse_json( reply1 )
    if parsed1 == None :
        print( "cannot parse payload" )
        sys.exit( 3 )

    try :
        content = parsed1[ 'contents' ]
    except :
        content = None
    if content == None :
        print( "no content received:" )
        print( reply1 )
        sys.exit( 3 )

    selected = select_item( content )
    if len( selected ) == 0 :
        sys.exit( 3 )

    print( "you selected: {}".format( selected ) )
    ( status2, reply2 ) = requesting( selected, cart, drs_url )
    if status2 == None :
        print( "2nd request to {} failed.".format( drs_url ) )
        sys.exit( 3 )

    if status2 != 200 :
        print( reply2 )
        sys.exit( 3 )

    parsed2 = try_parse_json( reply2 )
    if parsed2 == None :
        print( "cannot parse payload" )
        sys.exit( 3 )

    url2 = None
    checksum = None
    file_size = None
    try :
        url2 = parsed2[ 'access_methods' ][ 0 ][ 'access_url' ]
        checksum = parsed2[ 'checksums' ][ 0 ][ 'checksum' ]
        file_size = parsed2[ 'size' ]
    except :
        print( "cannot extract url, checksum, file_size:" )
        print( reply2 )
        sys.exit( 3 )
        
    print( "you get it from: {}\nchecksum={}\nsize={:,}".format( url2, checksum, file_size ) )
    if continue_or_cancel() != 1 :
        sys.exit( 3 )

    ( fsize, hash, elapsed ) = read_loop( url2, 1024 * 1024 )
    if hash == checksum :
        print( "\nchecksum: OK" )
    else :
        print( "\nchecksum: does not match" )
    if file_size == fsize :
        print( "size: OK" )
    else :
        print( "size: does not match" )
    print( "in {:.2f} seconds / {:,} bytes per second".format( elapsed, int( fsize / elapsed ) ) )

    print( "done." )

