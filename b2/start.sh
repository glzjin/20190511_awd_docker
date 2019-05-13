#!/bin/bash

service nginx start

su - glzjin -c "nohup python3 /home/glzjin/Flaskshop/run.py &"
