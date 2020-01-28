FROM ubuntu:latest
# Currently LTS (5 year support). 18.04 likely will roll to 20.04

LABEL author="Mike Vartanian"
MAINTAINER mike.vartanian@nih.gov


USER root
RUN apt-get -q update -y && \
    apt-get -q upgrade -q -y && \
    apt-get -q install -q -y curl docker python3 python3-pip \
             shellcheck jq protobuf-compiler docker.io \
             git openjdk-11-jre-headless wget

RUN pip3 -q install connexion python_dateutil setuptools \
             flask_testing coverage \
             nose pluggy py randomize black pylint pre-commit \
             uwsgi protobuf


RUN wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | apt-key add -
RUN sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'


RUN apt-get -y -q update && \
    apt-get -y -q install jenkins

RUN usermod -aG docker jenkins

RUN service jenkins stop

USER jenkins

RUN mkdir -p /var/lib/jenkins/jobs/ncbi-drs/
COPY config.xml /var/lib/jenkins/jobs/config.xml

#COPY jenkins.tar /var/lib/jenkins/jenkins.tar
#COPY run_jenkins.sh /var/lib/jenkins/run_jenkins.sh

#CMD ["/var/lib/jenkins/run_jenkins.sh"]


COPY jenkins_drs.tar /tmp/jenkins.tar

USER root
RUN  chmod go+r /tmp/jenkins.tar && cd /var/lib && tar -xf /tmp/jenkins.tar

EXPOSE 8080

CMD service jenkins start && tail -f /dev/null
