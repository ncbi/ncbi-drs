FROM alpine:latest AS setup
ENV PYTHONUNBUFFERED=1
RUN apk add --no-cache \
    python3 uwsgi-python3 py3-pip sqlite

FROM setup AS builder
COPY requirements /tmp/requirements
COPY src ga4gh
COPY data-repository-service-schemas/openapi/data_repository_service.swagger.yaml \
     ga4gh/drs/openapi/data_repository_service.swagger.yaml
COPY setup /tmp/setup
RUN cat /tmp/setup/makedb.sql /tmp/setup/data.sql | sqlite3 /var/DRS.sqlite && \
    rm -rf /tmp/setup
RUN pip3 install --no-cache --requirement /tmp/requirements/base.txt
ENV DRS_DB=/var/DRS.sqlite
ENV PYTHONPATH=ga4gh

FROM builder AS runner
EXPOSE 80
CMD ["uwsgi", "--master", \
     "--http-socket", ":80", \
     "--uid", "uwsgi", \
     "--plugins", "python3", \
     "--wsgi", "ga4gh.drs.main"]

FROM builder AS tester
RUN pip3 install --no-cache --requirement /tmp/requirements/test.txt
COPY tests tests
ENV PYTHONUNBUFFERED=0
CMD ["pytest", "-v", "-rsx", "tests"]
