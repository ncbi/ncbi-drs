# ncbi-drs

An implementation of GA4GH's Data Repository Service (DRS).

# If running on Ubuntu 18.04 LTS (recommended):
```bash
sudo apt-get install python3 python3-pip shellcheck jq protobuf-compiler
```

# If running on Amazon Linux 2:
```bash
sudo yum -y install python3-devel git gcc-c++ docker
# git clone this repo
cd ncbi-drs
pip3 install -r requirements.txt -r test-requirements.txt
sudo service docker start
sudo usermod -a -G docker ec2-user
# logout and log back in
```

# Python prerequisites
```bash
pip3 install -r requirements.txt -r test-requirements.txt
~/.local/bin/pre-commit install
```

# Pre-commit flight check
```bash
pre-commit run --all-files
```

# To build outside Jenkins:
```bash
$ ./build.sh
```

# To run tests, container will listen on external port 443 for firewall reasons
```bash
$ ./test.sh
```
