#!/bin/bash

echo "Running makemigrations"
python manage.py makemigrations

echo "Running migrations"
python manage.py migrate

python manage.py collectstatic --noinput

echo "Running server"
python manage.py runserver 0.0.0.0:8000