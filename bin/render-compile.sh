#!/usr/bin/env bash
set -o errexit

echo "-----> Install dependencies"
pip install -r requirements.txt

echo "-----> Running static files collection"
python manage.py collectstatic --noinput

echo "-----> Running database migration"
python manage.py migrate --noinput

echo "-----> Running dynamic preferences checks"
python manage.py checkpreferences

echo "-----> Running static asset compilation"
npm install -g @vue/cli-service-global
npm install
npm run build

echo "-----> Post-compile done"
