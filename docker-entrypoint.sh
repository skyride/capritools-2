#!/bin/sh

cp capritools/local_settings.docker capritools/local_settings.py
python manage.py migrate
python import.py

exec "$@"