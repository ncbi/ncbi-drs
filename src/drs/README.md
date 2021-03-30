This is the DRS Server. Setup code is in `main.py`. `server.py` contains the API entry points.
`db.py` contains the database access that does the **real** work with the DRS IDs.

The `DRS_Request` object in `server.py` is the skeleton of the server. It contains 3 static 
methods of particular interest to anyone wanting to make a real implementation.

1. `call_db` that calls the database code.
1. `call_ras` for handling permissions tokens.
1. `call_url_signer` for generating signed URLs.

The last 2 are stubs that will raise an exception if called.
These stubs are also useful as targets for `unittest.mock` in making unit tests.
