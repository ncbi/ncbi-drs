FROM alpine:latest AS setup
ENV PYTHONUNBUFFERED=1
COPY requirements /tmp/requirements
RUN apk add --no-cache build-base util-linux linux-headers \
    python3 py3-pip python3-dev && \
    /usr/bin/pip install --no-cache --upgrade pip setuptools wheel && \
    /usr/bin/pip install --no-cache --requirement /tmp/requirements/base.txt
    
FROM setup AS builder
COPY src src
COPY data-repository-service-schemas/openapi/data_repository_service.swagger.yaml \
     src/drs/openapi/data_repository_service.swagger.yaml
RUN sed -e '/x-swagger-router-controller/ s/ga4gh.//' -i src/drs/openapi/data_repository_service.swagger.yaml
     
FROM builder AS runner
EXPOSE 80
ENV PYTHONPATH=src
CMD /usr/bin/uwsgi --http-socket :80 --master --module src.drs.main

FROM builder AS tester
RUN /usr/bin/pip install --no-cache --requirement /tmp/requirements/test.txt
COPY tests tests
ENV PYTHONUNBUFFERED=0
ENV PYTHONPATH=src
CMD ["pytest", "-v", "-rsx", "tests"]
