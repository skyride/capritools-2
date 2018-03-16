#!/bin/bash

cp capritools/local_settings.docker capritools/local_settings.py
python manage.py migrate

if [ "$IMPORT" = True ] ; then
    python import.py
fi


exec "$@"