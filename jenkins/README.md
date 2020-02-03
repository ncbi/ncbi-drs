# Jenkins in docker

tl;dr

Run docker with **`-v /var/run/docker.sock:/var/run/docker.sock`** to forward docker-in-docker to the host.

## EC2 Setup

Starting with a basic AMI, e.g. amzn2-ami-hvm-2.0.20191217.0-x86_64-gp2 (ami-062f7200baf2fa504)

#### Install docker
```
sudo amazon-linux-extras install docker
sudo service docker start
sudo usermod -aG docker ec2-user
```
Log out and back in. Run `docker info` to verify docker is up and running.

#### Make docker daemon socket writable to all

```
sudo chmod ugo+w /var/run/docker.sock
```

#### Build the dockerfile

```
git clone <this/repo>
cd <this/repo/jenkins>
# scp ~vartanianmh/jenkins_drs.tar ec2user@ip:ncbi-drs/jenkins
docker build -t jenkins .
```

#### Start Jenkins docker

```
docker run --detach --network host --volume /var/run/docker.sock:/var/run/docker.sock jenkins

sudo iptables -A PREROUTING -t nat -i eth0 -p tcp --dport 443 -j REDIRECT --to-port 8080

sudo iptables -A PREROUTING -t nat -i ens5 -p tcp --dport 443 -j REDIRECT --to-port 8080
```

Jenkins should now be running on http://1.2.3.4:443/

----

### See:

[Using Docker-in-Docker for your CI or testing environment? Think twice.](http://jpetazzo.github.io/2015/09/03/do-not-use-docker-in-docker-for-ci/)
