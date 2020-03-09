FROM ubuntu:latest

LABEL author="Kenneth Durbrow" maintainer="kenneth.durbrow@nih.gov"

RUN apt-get -qq update && apt-get -qq install -y \
    apache2 \
    libapache2-mod-wsgi-py3 \
    python3-pip \
 >> /dev/null \
 && pip3 -q install \
    connexion \
 && rm -rf /var/lib/apt/lists \
 && rm `find /var/log -type f`

COPY files/ /
COPY source /var/www/wsgi-scripts/ga4gh/drs
RUN echo \
    "ServerName 127.0.0.1:80\n" \
    "LogLevel info\n" \
    "ServerSignature Off\n" \
    "ServerTokens Prod\n" >> /etc/apache2/apache2.conf \
 && rm -f /var/www/wsgi-scripts/ga4gh/drs/test_values.py \
 && chmod 755 `find /var/www -type f`

EXPOSE 80

CMD ["/usr/sbin/apache2ctl", "-DFOREGROUND"]
