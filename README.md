# ncbi-drs

A serverless (AWS Lambda) Flask (Python3.8) implementation of GA4GH's Data
Repository Service (DRS).

# Pre-commit
pip install pre-commit
pre-commit install

# Pre-commit flight check
pre-commit run --all-files

# To build outside jenkins:
$ ./build.sh

# To run tests, container will listen on external port 443 for firewall reasons
$ ./test.sh
