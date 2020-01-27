FROM jenkins/jenkins:lts

LABEL author="Kenneth Durbrow"
MAINTAINER kenneth.durbrow@nih.gov

# install docker
USER root
RUN apt-get update -y && apt-get upgrade -y && \
    apt-get -q install -y -q curl
RUN curl -fsSL https://get.docker.com | sh
RUN usermod -aG docker jenkins
USER jenkins
# expect this to fail because the docker daemon is not running
RUN docker version || true

RUN mkdir -p $JENKINS_HOME/jobs/ncbi-drs/
COPY config.xml /var/lib/jenkins/jobs/config.xml
#COPY jenkins.tar /var/lib/jenkins/jenkins.tar
#COPY run_jenkins.sh /var/lib/jenkins/run_jenkins.sh

#CMD ["/var/lib/jenkins/run_jenkins.sh"]
