FROM ubuntu:latest
# Currently LTS (5 year support). 18.04 likely will roll to 20.04

LABEL author="Mike Vartanian"
MAINTAINER mike.vartanian@nih.gov

RUN apt-get update && \
    apt-get -q -y install python3 apache2 \
                  curl libapache2-mod-wsgi-py3 python3-pip \
                  jq protobuf-compiler

COPY requirements.txt /tmp/requirements.txt
COPY test-requirements.txt /tmp/test-requirements.txt
RUN pip3 -q install -r /tmp/requirements.txt -r /tmp/test-requirements.txt

RUN echo "Empty" > /var/www/html/index.html
COPY favicon.ico /var/www/favicon.ico
RUN chmod 755 /var/www/favicon.ico

RUN mkdir -p /var/www/wsgi-scripts/ga4gh/drs /var/www/wsgi-scripts/templates
COPY drs.py /var/www/wsgi-scripts/drs.py
COPY ga4gh/ /var/www/wsgi-scripts/ga4gh/
COPY openapi/data_repository_service.swagger.yaml /var/www/wsgi-scripts/openapi/data_repository_service.swagger.yaml
COPY templates/home.html /var/www/wsgi-scripts/templates/home.html
RUN chmod 755 /var/www/wsgi-scripts/drs.py \
        /var/www/wsgi-scripts/ga4gh/drs/server.py \
        /var/www/wsgi-scripts/openapi/data_repository_service.swagger.yaml \
        /var/www/wsgi-scripts/templates/home.html \
        /var/www/wsgi-scripts/


COPY wsgi.conf /etc/apache2/mods-enabled/wsgi.conf
RUN mkdir -p /etc/apache2/conf
RUN echo "ServerName 127.0.0.1:80" >> /etc/apache2/apache2.conf
RUN echo "LogLevel info" >> /etc/apache2/apache2.conf
RUN echo "ServerSignature Off" >> /etc/apache2/apache2.conf
RUN echo "ServerTokens Prod" >> /etc/apache2/apache2.conf

EXPOSE 80

CMD /usr/sbin/apache2ctl -D FOREGROUND

# Docker hints
# ____________
#
# sudo docker build - < Dockerfile
# sudo docker build -t ubuntu . # Creates image
# sudo docker images # Lists images
# sudo docker save -o out.tar image # image to tar
# sudo docker run -it image-id # Creates container from image and runs
# CAn also docker create and then docker start
# sudo docker run -it image-id bash # debugging
# sudo docker ps # Shows "running" containers
# docker exec -it container-id bash # Attach to running container
# docker commit goes from container back to image


# Cleanup
# sudo docker rm -f $(sudo docker ps -a -q)
# sudo docker rmi $(sudo docker images -q)
# docker container prune -f
# docker image prune -a -f
