#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgresql..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python src/manage.py makemigrations
python src/manage.py migrate

exec "$@"
