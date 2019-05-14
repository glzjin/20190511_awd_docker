FROM ubuntu:14.04

COPY html/ /var/www/html/

RUN sed -i 's/http:\/\/archive.ubuntu.com\/ubuntu\//http:\/\/mirrors.tuna.tsinghua.edu.cn\/ubuntu\//g' /etc/apt/sources.list && \
    sed -i '/security/d' /etc/apt/sources.list && \
    apt-get update -y && \
    apt-get -yqq install supervisor mariadb-server apache2 php5 libapache2-mod-php5 \
    php5-mysql php5-mcrypt ssh && \
    # config
    sed -i "154s/Indexes//" /etc/apache2/apache2.conf && \
    sed -i "165s/Indexes//" /etc/apache2/apache2.conf && \
    /etc/init.d/apache2 start && \
    # mysql
    rm -rf /var/lib/mysql && \
    mysql_install_db --user=mysql --datadir=/var/lib/mysql && \
    sh -c 'mysqld_safe &' && \
    sleep 5s  && \
    mysqladmin -uroot password '334cc35b3c704593' && \
    mysql -e "source /var/www/html/geez.sql;" -uroot -p334cc35b3c704593
    # supervisor
RUN mkdir -p /var/log/supervisor && \
    mv /var/www/html/supervisord.conf /etc/ && \
    #
    chown -R www-data:www-data /var/www/html/ && \
    chmod -R 755 /var/www/html/ && \
    rm /var/www/html/geez.sql /var/www/html/index.html && \
    cat /dev/null > /var/www/html/log.php

RUN sed -ri 's/^#?PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN useradd -g www-data glzjin -m && \
    password=$(openssl passwd -1 -salt 'abcdefg' '123456') && \
    sed -i 's/^glzjin:!/glzjin:'$password'/g' /etc/shadow

RUN chmod -R 777 /var/www/html

RUN mkdir /var/run/sshd

RUN echo 'flag{glzjin_wants_a_girl_friend}' > /flag.txt

EXPOSE 80
EXPOSE 22

ENTRYPOINT ["supervisord", "-n"]
