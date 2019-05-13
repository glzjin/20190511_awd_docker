FROM phusion/baseimage

RUN rm -f /etc/service/sshd/down
RUN sed -ri 's/^#?PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config

ADD ./mysql-passwd /tmp/
ADD ./sources.list /etc/apt/
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 14AA40EC0831756756D7F66C4F4EA0AAE5267A6C
RUN apt update
RUN apt install nginx -y
RUN debconf-set-selections /tmp/mysql-passwd && apt install mysql-server -y
RUN rm -rf /tmp/mysql-passwd

RUN apt install php5.6-fpm php5.6-mysql -y

ADD init_db.sh /tmp/init_db.sh
RUN chmod u+x /tmp/init_db.sh
ADD ./init.sql /root/
RUN /tmp/init_db.sh

ADD ./default /etc/nginx/sites-enabled/

RUN useradd -g www-data glzjin -m && \
    password=$(openssl passwd -1 -salt 'abcdefg' '123456') && \
    sed -i 's/^glzjin:!/glzjin:'$password'/g' /etc/shadow

RUN rm -f /var/www/html/index.html
COPY ./html /var/www/html/
RUN chown -R glzjin:www-data /var/www/html/
RUN chmod -R 777 /var/www/html/


RUN echo 'flag{glzjin_wants_a_girl_friend}' > /flag.txt

ADD ./start.sh /etc/my_init.d/
RUN chmod u+x /etc/my_init.d/start.sh
