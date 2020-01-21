FROM ubuntu:latest
# Currently LTS (5 year support). 18.04 likely will roll to 20.04

LABEL author="Mike Vartanian"
MAINTAINER mike.vartanian@nih.gov

RUN apt-get update -y && apt-get upgrade -y && \
    apt-get -q install -y -q python3  python3-pip git openjdk-11-jre-headless wget
RUN wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | apt-key add - > /dev/null 2>&1
RUN echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list
RUN apt-get update -y && apt-get upgrade -y && apt-get install -y jenkins


RUN mkdir -p $JENKINS_HOME/jobs/ncbi-drs/
COPY jenkins.tar /var/lib/jenkins/jenkins.tar
COPY config.xml /var/lib/jenkins/jobs/config.xml
COPY run_jenkins.sh /var/lib/jenkins/run_jenkins.sh

CMD ["/var/lib/jenkins/run_jenkins.sh"]
