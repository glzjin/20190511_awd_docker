FROM phusion/baseimage

RUN rm -f /etc/service/sshd/down
RUN sed -ri 's/^#?PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config

RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirrors.aliyun.com/g" /etc/apt/sources.list
RUN apt update
RUN apt install nginx -y
RUN apt install python3 -y

RUN curl https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
RUN python3 /tmp/get-pip.py

RUN pip3 install Flask
RUN pip3 install flask_sqlalchemy
RUN pip3 install flask_bcrypt
RUN pip3 install flask_login
RUN pip3 install flask_mail
RUN pip3 install flask_wtf
RUN pip3 install pyyaml==3.12

ADD ./default /etc/nginx/sites-enabled/

RUN groupadd glzjin && \
    useradd -g glzjin glzjin -m && \
    password=$(openssl passwd -1 -salt 'abcdefg' '123456') && \
    sed -i 's/^glzjin:!/glzjin:'$password'/g' /etc/shadow

RUN mkdir /home/glzjin/Flaskshop
COPY ./Flaskshop/ /home/glzjin/Flaskshop/
RUN chown -R glzjin:glzjin /home/glzjin/Flaskshop/

RUN echo 'flag{glzjin_wants_a_girl_friend}' > /flag.txt

ADD ./start.sh /etc/my_init.d/
RUN chmod u+x /etc/my_init.d/start.sh
