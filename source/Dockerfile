FROM alpine:latest

LABEL author="Kenneth Durbrow" maintainer="kenneth.durbrow@nih.gov"

RUN apk update && \
    apk add python3 && \
    pip3 -q install connexion pytest

RUN mkdir /source
WORKDIR /source
VOLUME /source

CMD pytest -o cache_dir=/tmp \
    server.py \
    token_extract.py \
    cloud.py \
    proxy.py \
    rewrite.py
