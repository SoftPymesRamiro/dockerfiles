#!/bin/bash
nohup service nginx start
cd /root/app/ && nohup webpack --progress --watch > /root/logs/log.txt 

