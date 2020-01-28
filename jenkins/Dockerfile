FROM jenkins/jenkins:lts

LABEL author="Mike Vartanian"
MAINTAINER mike.vartanian@nih.gov

# install docker
USER root
RUN apt-get update -y && apt-get upgrade -y && \
    apt-get -q install -y -q curl docker.io python3 python3-pip \
             shellcheck jq protobuf-compiler

RUN curl -fsSL https://get.docker.com | sh

RUN usermod -aG docker jenkins

RUN pip3 install connexion python_dateutil setuptools \
             flask_testing coverage \
             nose pluggy py randomize black pylint pre-commit \
             uwsgi protobuf

USER jenkins
# expect this to fail because the docker daemon is not running
RUN docker version || true

RUN mkdir -p $JENKINS_HOME/jobs/ncbi-drs/
COPY config.xml /var/lib/jenkins/jobs/config.xml

#COPY jenkins.tar /var/lib/jenkins/jenkins.tar
#COPY run_jenkins.sh /var/lib/jenkins/run_jenkins.sh

#CMD ["/var/lib/jenkins/run_jenkins.sh"]
