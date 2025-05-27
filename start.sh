#!/usr/bin/env bash
python manage.py collectstatic --noinput
python manage.py migrate --noinput
gunicorn tabbycat.wsgi:application --bind 0.0.0.0:$PORT
