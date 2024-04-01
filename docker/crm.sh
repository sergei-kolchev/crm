#!/bin/bash

echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate --noinput

# Create superuser
echo "Creating superuser"
if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL
fi

# Start gunicorn
echo "Starting gunicorn"
gunicorn crm.wsgi:application --workers 1 --bind=0.0.0.0:8000 --timeout 90