FROM jenkins/jenkins:lts
LABEL maintainer="mvartanian@ncbi.nlm.nih.gov"

# docker build  -t drsjenkins .
# docker run -p 443:8080 -p 50000:50000 drsjenkins
# docker run -p 443:8080 --mount source=drs,target=/var/jenkins_home jenkins/jenkins:lts
# docker cp id:/var/jenkins_home - > snap.tar

USER root
RUN apt-get update && apt-get install -y
USER jenkins
RUN mkdir -p $JENKINS_HOME/jobs/ncbi-drs/
COPY new.tar /usr/share/jenkins/ref/new.tar
RUN cd /usr/share/jenkins/ref && tar -xvf new.tar && ls -la
RUN mkdir -p /usr/share/jenkins/ref/jobs
COPY config.xml /usr/share/jenkins/ref/jobs
