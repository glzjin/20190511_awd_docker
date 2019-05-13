FROM phusion/baseimage

RUN rm -f /etc/service/sshd/down
RUN sed -ri 's/^#?PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config

ADD ./mysql-passwd /tmp/
RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirrors.aliyun.com/g" /etc/apt/sources.list
RUN apt update
RUN apt install apache2 -y
RUN debconf-set-selections /tmp/mysql-passwd && apt install mysql-server -y
RUN rm -rf /tmp/mysql-passwd
RUN apt install php libapache2-mod-php php-mcrypt php-mysql php-gd -y

ADD init_db.sh /tmp/init_db.sh
RUN chmod u+x /tmp/init_db.sh
ADD ./init.sql /root/
RUN /tmp/init_db.sh

RUN useradd -g www-data glzjin -m && \
    password=$(openssl passwd -1 -salt 'abcdefg' '123456') && \
    sed -i 's/^glzjin:!/glzjin:'$password'/g' /etc/shadow

RUN rm -f /var/www/html/index.html
COPY ./html /var/www/html/
RUN chown -R glzjin:www-data /var/www/html/
RUN chmod -R 777 /var/www/html/

COPY 000-default.conf /etc/apache2/sites-enabled/
COPY apache2.conf /etc/apache2/
RUN ln -s /etc/apache2/mods-available/rewrite.load /etc/apache2/mods-enabled/

RUN echo 'flag{glzjin_wants_a_girl_friend}' > /flag.txt

ADD ./start.sh /etc/my_init.d/
RUN chmod u+x /etc/my_init.d/start.sh
