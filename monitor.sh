#!/bin/bash

while true;do    
    date
    python /data0/logs/wmsadminapi/monitor.py
    sleep 600
done
