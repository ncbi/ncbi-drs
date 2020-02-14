# ncbi-drs

An implementation of GA4GH's Data Repository Service (DRS).

# If running on Ubuntu 18.04 LTS (recommended):
```bash
sudo apt-get install python3 python3-pip shellcheck jq protobuf-compiler
# git clone this repo
cd ncbi-drs
pip3 install -r requirements.txt -r test-requirements.txt
~/.local/bin/pre-commit install
```

# If running on Amazon Linux 2:
```bash
sudo yum -y install python3-devel git gcc-c++ docker
sudo service docker start
sudo usermod -a -G docker ec2-user
# git clone this repo
cd ncbi-drs
sudo pip3 install -r requirements.txt -r test-requirements.txt
pre-commit install
# logout and log back in before running docker scripts
```

# Pre-commit flight check
```bash
pre-commit run --all-files
```

# To build docker containers outside Jenkins:
```bash
./package.sh
```

# To run tests, container will listen on external port 443 for firewall reasons
```bash
./test.sh
```
