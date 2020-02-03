FROM ubuntu:latest

LABEL author="Kenneth Durbrow" maintainer="kenneth.durbrow@nih.gov"

RUN apt-get update && \
    apt-get -q -y install python3 python3-pip

RUN pip3 -q install connexion  python_dateutil
