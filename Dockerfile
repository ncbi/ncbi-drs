FROM centos:8
LABEL author="Mike Vartanian"
MAINTAINER mike.vartanian@nih.gov

RUN yum -y --exclude=kernel.* update
RUN yum -y install python3 httpd mod_wsgi git
RUN pip3 install connexion python_dateutil setuptools \
             flask_testing coverage \
             nose pluggy py randomize black pylint

# Apache conf
RUN sed -i -r 's@#(LoadModule rewrite_module modules/mod_rewrite.so)@\1@i' /etc/apache2/httpd.conf
RUN sed -i -r 's@Errorlog .*@Errorlog /dev/stderr@i' /etc/apache2/httpd.conf
RUN sed -i -r 's@#Servername.*@Servername wsgi@i' /etc/apache2/httpd.conf
RUN echo -e "Transferlog /dev/stdout\n\
LoadModule wsgi_module modules/mod_wsgi.so\n\
WSGIPythonPath /usr/lib/python3.6\n\
Alias / /srv/\n\
<Directory /srv>\n\
    Options ExecCGI Indexes FollowSymLinks\n\
    AllowOverride All\n\
    Require all granted\n\
    AddHandler wsgi-script .wsgi\n\
</Directory>" >> /etc/apache2/httpd.conf

RUN mkdir -p /run/apache2

WORKDIR /srv
EXPOSE 80

ONBUILD COPY . /srv

CMD ["httpd", "-D", "FOREGROUND", "-e", "info"]

