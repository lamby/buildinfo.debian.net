#!/bin/sh
bidb/manage.py migrate
exec python bidb/manage.py runserver 0.0.0.0:8000
