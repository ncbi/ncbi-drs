# ncbi-drs

An implementation of GA4GH's Data Repository Service (DRS) on top of NCBI's SRA
Data Locator (SDL).

## Running the service:

### Build the image.
```sh
docker build -t ncbi-drs .
```

### Run the container.
```sh
docker run --detach --publish 8080:80 --name ncbi-drs --rm ncbi-drs
```
Note: The actual port (in this example, 8080) is up to you.

### Test that the service is running.
```sh
curl http://localhost:8080/ga4gh/drs/v1/objects/SRR000000
```
This will produce a canned response. This only tests that the service is
running. (Note: SRR000000 is not a real SRA accession.)

### Test that the service is running and talking to NCBI's SDL service.
```sh
curl http://localhost:8080/ga4gh/drs/v1/objects/SRR000001
```
This should produce a real response. This tests that the service is running and
can talk to NCBI to perform lookups. (Note: SRR000001 is a real SRA accession
containing public data.)

This is as far as you can test with public data.

## Accessing protected dbGaP data

*The details of accessing protected dbGaP data through this service are in flux,
this is for illustration purposes only.*

You can access protected dbGaP data by providing a dbGaP access token as a
bearer token in the HTTP Authentication header. For example:
```sh
curl -H "Authorization: Bearer @/path/to/token" http://localhost:8080/ga4gh/drs/v1/objects/SRR000001
```

dbGaP has a test project that consists of publicly available data. Anyone can
get access to this data. See [dbGaP project: 1000 Genomes Used for Cloud Testing](https://trace.ncbi.nlm.nih.gov/Traces/study/?dbgap_project=0)

## A Note about the DRS IDs used by this service

This service recognizes SRA run accessions (e.g. SRR, ERR, and DRR followed by a
string of digits) as bundle IDs and returns a contents array. The IDs in that
array can then be used to request access URLs to the individual files.

### Why only run accessions?

The complete set of SRA accessions do not correspond to DRS IDs. SRA accessions
represent objects such as submissions, experiments, studies, and projects. These
objects are long-lived and their contents **can change over time**. This makes
them unsuitable as DRS IDs. Generally, these changes are additive, but a
researcher can submit new data to replace their previous submission. Generally,
these changes happen in recent (or active) projects with the old ones being
stable, but this is not guaranteed. So at this time, we can not properly support
DRS IDs, and we do not wish to issue invalid IDs. However, using run accessions,
we can come very close to something that mostly works as expected.

## Some technical details

Protected dbGaP files are only available from the SRA via signed URLs to cloud
storage buckets (or from NCBI as encrypted files). Due to issues regarding
security and egress charges, this service does not hand out the signed URLs
directly. When a signed URL is encountered, this service hands out a URL to
itself. That URL leads to a transparent proxy that will perform the retrieval.
Any egress charges will accrue to the account that is running this service and
not to the account that owns the bucket.

This Dockerfile builds for ubuntu's configuration of Apache, it is particular
and sensitive to that.

This service is implemented in Python and Flask.

## Hopefully useful information:

### If running on Amazon Linux 2,

Install docker, see [Docker Basics for Amazon ECS](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/docker-basics.html)
