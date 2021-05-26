#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DJANGO_SQL_HOST $DJANGO_SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py collectstatic --no-input
python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate
python manage.py initadmin $DJANGO_ADMIN_NAME $DJANGO_ADMIN_PASSWORD

exec "$@"
