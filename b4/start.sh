#!/bin/bash

service nginx start

service php5.6-fpm start

find /var/lib/mysql -type f -exec touch {} \; && service mysql start
