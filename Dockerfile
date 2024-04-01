FROM python:3.11

ENV CRM_SETTINGS_PATH=PROD
RUN mkdir /crm
WORKDIR /crm
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY crm .
COPY docker docker
RUN chmod a+x docker/*.sh