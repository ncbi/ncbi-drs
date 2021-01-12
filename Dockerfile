FROM alpine:latest AS setup
ENV PYTHONUNBUFFERED=1
COPY requirements /tmp/requirements
RUN apk add --no-cache build-base util-linux linux-headers g++ \
    python3 py3-pip uwsgi-python3 && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
    pip3 install --no-cache --upgrade pip setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -sf pip3 /usr/bin/pip ; fi && \
    pip install --no-cache --requirement /tmp/requirements/base.txt
    
FROM setup AS builder
COPY src src
COPY data-repository-service-schemas/openapi/data_repository_service.swagger.yaml \
     src/drs/openapi/data_repository_service.swagger.yaml
RUN sed -e '/x-swagger-router-controller/ s/ga4gh.//' -i src/drs/openapi/data_repository_service.swagger.yaml
     
FROM builder AS runner
EXPOSE 80
CMD ["uwsgi", "--http-socket" ":80", "--master", "--module", "drs.main"]

FROM builder AS tester
RUN pip install --no-cache --requirement /tmp/requirements/test.txt
COPY tests tests
ENV PYTHONUNBUFFERED=0
ENV PYTHONPATH=src
CMD ["pytest", "-v", "-rsx", "tests"]
