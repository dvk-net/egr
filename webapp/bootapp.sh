#!/usr/bin/env bash
cd ./src
echo "yes" | python3 manage.py collectstatic
python3 manage.py migrate --noinput
gunicorn -w 3 proj.wsgi --bind 0.0.0.0:8000 --timeout 6000
