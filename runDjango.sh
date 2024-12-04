#!/bin/bash
#nohup sudo python3 /home/kenchou2006/WarningSign\ 2.0/server/manage.py runserver 0.0.0.0:80
sudo gunicorn --bind 0.0.0.0:443 --certfile=server.crt --keyfile=server.key server.wsgi