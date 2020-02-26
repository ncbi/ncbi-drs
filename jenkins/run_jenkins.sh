#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob globstar

id
cd /var/lib/jenkins
pwd
tar -xf ~/ncbi-drs/jenkins.tar
mkdir -p /var/lib/jenkins/jobs/ncbi-drs
ls -la
#cp config.xml /var/lib/jenkins/jobs


/usr/bin/java -Djava.awt.headless=true \
    -jar /usr/share/jenkins/jenkins.war \
    --webroot=/var/cache/jenkins/war \
    --httpPort=8080

tail -f /dev/null
exit 0
