FROM ubuntu:latest

LABEL author="Kenneth Durbrow" maintainer="kenneth.durbrow@nih.gov"

#RUN apk update && apk upgrade 
#RUN apk add --no-cache python3
RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y python3 python3-pip

RUN pip3 -q install connexion  python_dateutil 
