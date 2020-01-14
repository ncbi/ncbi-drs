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

RUN echo "Empty" > /var/www/html/index.html

RUN mkdir -p /var/www/wsgi-scripts/
COPY application.py /var/www/wsgi-scripts/application.py
RUN chmod 755 /var/www/wsgi-scripts/application.py

COPY wsgi.conf /etc/apache2/mods-enabled/wsgi.conf
RUN mkdir -p /etc/apache2/conf
RUN echo "ServerName 127.0.0.1:80" >> /etc/apache2/apache2.conf
RUN echo "LogLevel info" >> /etc/apache2/apache2.conf
RUN echo "ServerSignature Off" >> /etc/apache2/apache2.conf

#WSGIScriptAlias /path file.py


#RUN systemctl restart apache2

WORKDIR /srv

EXPOSE 80

ONBUILD COPY . /srv

CMD /usr/sbin/apache2ctl -D FOREGROUND
