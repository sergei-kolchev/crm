FROM python:3.11

ENV CRM_SETTINGS_PATH=PROD

RUN mkdir /crm

WORKDIR /crm

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY crm .
COPY docker docker

RUN chmod a+x docker/*.sh

# RUN python manage.py collectstatic --noinput
# RUN python manage.py migrate
# RUN python manage.py loaddata
# make superuser

# EXPOSE 8000

# ENTRYPOINT ["docker/crm.sh"]

# CMD ["gunicorn", "crm.wsgi:application", "--workers", "1", "--bind", "0.0.0.0:8000", "--timeout", "90"]
