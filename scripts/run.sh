#!/bin/sh

python manage.py wait_for_db

python manage.py migrate
python manage.py collectstatic --noinput
python manage.py init_superuser

gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2 --threads 2
