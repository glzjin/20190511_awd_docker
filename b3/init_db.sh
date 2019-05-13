#!/bin/bash
chown -R mysql:mysql /var/lib/mysql
/etc/init.d/mysql start
sleep 5
echo `service mysql status`

mysql -uroot -proot < /root/init.sql

rm -rf /root/init.sql
rm -rf /tmp/init_db.sh
