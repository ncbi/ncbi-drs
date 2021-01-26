/* These tables represent the data, e.g. locations, status, permissions, etc */
CREATE TABLE Buckets (
    bucketID INTEGER PRIMARY KEY,
    bucketName TEXT NOT NULL,
    bucketProvider TEXT NOT NULL,
    bucketRegion TEXT NOT NULL,
    bucketSigningAccount TEXT NULL,
    bucketIsUserPays INTEGER NOT NULL DEFAULT ( 0 )
);

CREATE TABLE FileStates (
    stateName TEXT NOT NULL UNIQUE,
    stateDescription TEXT
);
INSERT INTO FileStates VALUES ( 'online', 'Online' );
INSERT INTO FileStates VALUES ( 'offline', 'Moved to offline storage' );
INSERT INTO FileStates VALUES ( 'unpublished', 'Not yet published' );
INSERT INTO FileStates VALUES ( 'withdrawn', 'Withdrawn from publication' );
INSERT INTO FileStates VALUES ( 'removed', 'Deleted' );

CREATE TABLE FilePermissions (
    permName TEXT NOT NULL UNIQUE,
    permDescription TEXT
);
INSERT INTO FilePermissions VALUES ( 'public', 'Public Data' );

CREATE TABLE Files (
    fileID INTEGER PRIMARY KEY,
    fileName TEXT NOT NULL,
    fileMD5 TEXT NOT NULL,
    fileSize INT NOT NULL,
    fileDate TEXT NOT NULL,
    fileState INTEGER NOT NULL DEFAULT ( 1 ),
    filePermission INT NOT NULL DEFAULT ( 1 ) -- FilePermissions(ROWID)
);

CREATE TABLE FileLocations (
    flFileID INTEGER NOT NULL REFERENCES Files ( fileID ),
    flBucket INTEGER NOT NULL REFERENCES Buckets ( bucketID ),
    flURL TEXT NOT NULL,
    flState INTEGER NOT NULL DEFAULT ( 1 ),
    UNIQUE ( flFileID, flBucket ) ON CONFLICT ROLLBACK
);

/* These two tables represent the DRS metadata.
 *
 * It is intentional that the metadata may be
 * out of sync with the data.
 *
 * The DRS server needs to remember every ID it
 * ever replied with, but the data may change.
 *
 * The ID may not get you to the data, but the
 * server will still remember that it was once
 * a valid ID.
 */
CREATE TABLE Objects (
    objectID TEXT NOT NULL UNIQUE ON CONFLICT ROLLBACK, -- this is the DRS ID, it is also the checksum
    objectCreateTime TEXT NOT NULL, -- of file or most recent child
    objectSize INTEGER NOT NULL, -- size of file or sum of size of children
    objectFileID INTEGER NULL REFERENCES Files ( fileID ),
    objectName TEXT NULL -- informational
);

CREATE TABLE Containers (
    contParent INTEGER NOT NULL, -- Objects(ROWID)
    contChild INTEGER NOT NULL, -- Objects(ROWID)
    UNIQUE ( contParent, contChild ) ON CONFLICT ROLLBACK
);
