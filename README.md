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
