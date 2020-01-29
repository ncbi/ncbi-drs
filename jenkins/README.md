# EC2 Setup

Bring up an Ubuntu 18.04 AMI on an x86_64 instance with at
least 1GB of memory.
I suggest t3a.micro.

launch_ubuntu_jenkins_docker.sh will do all this from NCBI.

export IP_ADDR="ec2 ip address of your instance"

### Run:
```
sudo apt-get update -y

sudo apt-get upgrade -y

sudo apt-get install -y docker.io python3 python3-pip \
             git openjdk-11-jre-headless shellcheck jq \
             protobuf-compiler
```
Log out and back in. Run `docker info` to verify docker is up and running.

### Build the dockerfile:

```
sudo chmod ugo+w /var/run/docker.sock
sudo usermod -aG docker ubuntu

ssh -a2kx "ubuntu@$IP_ADDR" 'mkdir ncbi-drs'
scp /home/vartanianmh/jenkins_drs.tar "ubuntu@$IP_ADDR:ncbi-drs/jenkins.tar"
ssh -a2kx "ubuntu@$IP_ADDR"
git clone https://github.com/ncbi/ncbi-drs/
git checkout VDB-####
pip3 -q install -r /tmp/requirements.txt -r /tmp/test-requirements.txt
cd ncbi-drs/
~/.local/bin/pre-commit install

docker build -t jenkins -f jenkins/Dockerfile .

```
### Start Jenkins docker for real

```
docker run -v /var/run/docker.sock:/var/run/docker.sock -p 443:8080 jenkins &
```

Jenkins should now be running on http://$IP_ADDR:443/

### See: [Using Docker-in-Docker for your CI or testing environment? Think twice.](http://jpetazzo.github.io/2015/09/03/do-not-use-docker-in-docker-for-ci/)
