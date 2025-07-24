FROM phusion/baseimage:master-amd64

RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirrors.aliyun.com/g" /etc/apt/sources.list
RUN apt-get update && apt-get -y dist-upgrade
RUN apt-get install -y lib32z1 xinetd build-essential

RUN rm -f /etc/service/sshd/down && /etc/my_init.d/00_regen_ssh_host_keys.sh > /dev/null 2>&1
RUN sed -ri 's/^#?PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config

RUN groupadd glzjin && \
    useradd -g glzjin glzjin -m && \
    password=$(openssl passwd -1 -salt 'abcdefg' '123456') && \
    sed -i 's/^glzjin:!/glzjin:'$password'/g' /etc/shadow

COPY ./flag.txt /flag.txt
COPY ./calculator /home/glzjin/calculator
COPY ./ctf.xinetd /etc/xinetd.d/ctf

RUN chown glzjin:glzjin /home/glzjin/calculator && chmod 777 /home/glzjin/calculator

RUN echo 'ctf - nproc 1500' >>/etc/security/limits.conf

CMD exec /bin/bash -c "/etc/init.d/ssh start; /etc/init.d/xinetd start; trap : TERM INT; sleep infinity & wait"

EXPOSE 8888
EXPOSE 22
