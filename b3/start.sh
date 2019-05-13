#!/bin/bash

service apache2 start

find /var/lib/mysql -type f -exec touch {} \; && service mysql start
