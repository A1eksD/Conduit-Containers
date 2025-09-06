#!/bin/sh
python manage.py migrate

python manage.py createsuperuser --no-input

gunicorn projectname.wsgi:application --bind 0.0.0.0:8383