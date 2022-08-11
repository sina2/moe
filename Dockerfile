FROM centos:7

RUN set -x && \
    yum install -y git && \
    yum install -y httpd && \
    cd /var/www/cgi-bin && \
    git clone https://github.com/sina2/moe.git && \
    cd moe && \
    chmod 755 *.cgi && \
    chmod 777 Icon img moelog moelog/pass.cgi

RUN sed -i 's/80/8080/' /etc/httpd/conf/httpd.conf

CMD [ "/usr/sbin/httpd" ,"-D", "FOREGROUND" ]
