#!/bin/sh
python manage.py makemigrations && python manage.py migrate

python manage.py collectstatic --noinput

python manage.py createsuperuser --no-input

gunicorn conduit.wsgi:application --bind 0.0.0.0:8383
