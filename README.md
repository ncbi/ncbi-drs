# ncbi-drs

An implementation of GA4GH's Data Repository Service (DRS).

# Python prerequisites
pip3 install -r requirements.txt -r test-requirements.txt
~/.local/bin/pre-commit install

# Pre-commit flight check
pre-commit run --all-files

# To build outside Jenkins:
$ ./build.sh

# To run tests, container will listen on external port 443 for firewall reasons
$ ./test.sh
