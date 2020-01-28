# ncbi-drs

An implementation of GA4GH's Data Repository Service (DRS).

# Pre-commit
pip3 install -r requirements.txt
~/.local/bin/pre-commit install

# Pre-commit flight check
export AWS_SESSION_TOKEN=123 # dummy credential if no other found
~/.local/bin/pre-commit run --all-files

# To build outside Jenkins:
$ ./build.sh

# To run tests, container will listen on external port 443 for firewall reasons
$ ./test.sh
