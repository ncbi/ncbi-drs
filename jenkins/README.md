# EC2 Setup

Bring up a basic AMI, e.g. amzn2-ami-hvm-2.0.20191217.0-x86_64-gp2 (ami-062f7200baf2fa504)

### Run:
```
sudo amazon-linux-extras install docker
sudo service docker start
sudo usermod -aG docker ec2-user
```
Log out and back in. Run `docker info` to verify docker is up and running.

### Make docker daemon socket writable to all

```
sudo chmod ugo+w /var/run/docker.sock
```

### Build the dockerfile

```
git <this/repo>
cd <this/directory>
# scp ~vartanianmh/jenkins_drs.tar ec2user@ip:ncbi-drs/jenkins
docker build -t jenkins .
```

Note: you *should* see an error about the docker daemon not running.

### Start Jenkins docker for real

```
docker run -v /var/run/docker.sock:/var/run/docker.sock -p 443:8080 jenkins
```

Jenkins should now be running on http://1.2.3.4:443/

### See: [Using Docker-in-Docker for your CI or testing environment? Think twice.](http://jpetazzo.github.io/2015/09/03/do-not-use-docker-in-docker-for-ci/)
