INSERT INTO Buckets ( bucketName, bucketProvider, bucketRegion )
VALUES ( 'sra-pub-src-1', 's3', 'us-east-1' );
INSERT INTO Buckets ( bucketName, bucketProvider, bucketRegion )
VALUES ( 'sra-pub-src-1', 'gs', 'US' );

INSERT INTO Files ( fileName, fileMD5, fileSize, fileDate )
VALUES ( 
    'm110613_062130_42141_c100154882555500000315044108061125_s1_p0.bas.h5',
    'dbf554827136113a58d0d1c32ca29e81',
    1117392407,
    '2014-11-13 16:40:21'
);
INSERT INTO FileLocations ( flFileID, flBucket, flURL, flState )
VALUES ( 1, 1, 'https://sra-pub-src-1.s3.amazonaws.com/SRR287671/m110613_062130_42141_c100154882555500000315044108061125_s1_p0.bas.h5.1', 1 );
INSERT INTO FileLocations ( flFileID, flBucket, flURL, flState ) 
VALUES ( 1, 2, 'https://storage.googleapis.com/sra-pub-src-1/SRR287671/m110613_062130_42141_c100154882555500000315044108061125_s1_p0.bas.h5.1', 2 );

INSERT INTO Objects ( objectID, objectCreateTime, objectSize, objectFileID, objectName )
VALUES (
    'dbf554827136113a58d0d1c32ca29e81',
    '2014-11-13 16:40:21',
    1117392407,
    1,
    'm110613_062130_42141_c100154882555500000315044108061125_s1_p0.bas.h5'
);
INSERT INTO Objects ( objectID, objectCreateTime, objectSize, objectName )
VALUES (
    '7d0b9ed4958e876a6a50ef6ae134de0f',
    '2014-11-13 16:40:21',
    1117392407,
    'SRR287671'
);
INSERT INTO Containers VALUES ( 2, 1 );
