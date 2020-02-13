#to be executed on the VM at AWS or GCP

echo "stopping all running containers"
docker stop $(docker ps -a -q)

echo "removing all containers and images"
docker container prune -f
docker image prune -a -f
docker container ls -a
docker image ls -a

echo "updating from git"
git pull

echo "building and creating the image"
./build.sh
./package.sh

echo "running the newly build image"
docker run -p 80:80 --detach --name DRS1 drs

