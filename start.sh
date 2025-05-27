#!/usr/bin/env bash
#!/usr/bin/env bash
set -o errexit

echo "===> START.SH IS RUNNING <==="

PYTHONPATH=. python tabbycat/run-asgi.py

python manage.py collectstatic --noinput
python manage.py migrate --noinput
gunicorn tabbycat.wsgi:application --bind 0.0.0.0:$PORT
