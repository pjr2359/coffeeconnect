#!/bin/bash
cd /home/site/wwwroot
python -m pip install -r requirements.txt
gunicorn --bind=0.0.0.0:8000 --timeout 600 coffeeconnect.wsgi:application