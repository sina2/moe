FROM centos:7

RUN set -x && \
    dnf install -y git && \
    dnf install -y httpd && \
    cd /var/www/cgi-bin && \
    git clone https://github.com/sina2/moe.git && \
    cd moe && \
    chmod 755 *.cgi && \
    chmod 777 Icon img moelog moelog/pass.cgi

EXPOSE 80
CMD [ "/usr/sbin/httpd" ,"-D", "FOREGROUND" ]
