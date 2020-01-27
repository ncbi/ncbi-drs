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
cd <this/directory>
docker build .
```

Note: you *should* see an error about the docker daemon not running.

### Test that fake docker-in-docker is working

```
docker run -v /var/run/docker.sock:/var/run/docker.sock docker info
```
The output should look the same as if you ran `docker info` directly on the host.

### Start Jenkins docker for real

```
docker run -v /var/run/docker.sock:/var/run/docker.sock ...
```

Jenkins will run docker commands using host docker daemon.
