FROM ubuntu:latest
# Currently LTS (5 year support). 18.04 likely will roll to 20.04

LABEL author="Mike Vartanian"
MAINTAINER mike.vartanian@nih.gov

RUN apt-get -q update -y && apt-get -q -y upgrade && apt-get -q -y install python3 apache2 libapache2-mod-wsgi-py3 python3-pip

RUN pip3 -q install connexion python_dateutil setuptools \
             flask_testing coverage \
             nose pluggy py randomize black pylint

# Copy python script to /var/www/html
# Add to /etc/apache2/mods-enabled/mod-wsgi.conf

RUN rm -f /var/www/html/index.html
RUN mkdir -p /var/www/html/wsgi-scripts/

COPY application.py /var/www/html/wsgi-scripts/application.py
COPY wsgi.conf /etc/apache2/mods-enabled/wsgi.conf

RUN echo "ServerName 127.0.0.1:80" >> /etc/httpd/conf/httpd.conf
RUN chmod 755 /var/www/html/wsgi-scripts/application.py

#WSGIScriptAlias /path file.py


#RUN systemctl restart apache2

WORKDIR /srv

EXPOSE 80

ONBUILD COPY . /srv

CMD /usr/sbin/apache2ctl -D FOREGROUND
