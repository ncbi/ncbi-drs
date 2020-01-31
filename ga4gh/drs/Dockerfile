FROM alpine:latest

LABEL author="Kenneth Durbrow" maintainer="kenneth.durbrow@nih.gov"

RUN apk update && apk upgrade && apk add --no-cache python3

RUN pip3 -q install connexion  python_dateutil 
