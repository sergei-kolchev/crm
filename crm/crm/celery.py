import os

from celery import Celery

from crm import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm.settings")

broker = "amqp://{}:{}@{}:{}//".format(
    settings.RABBITMQ_DEFAULT_USER,
    settings.RABBITMQ_DEFAULT_PASS,
    settings.BROKER_HOSTPORT,
    settings.BROKER_PORT,
)

app = Celery(
    settings.REDIS_NAME,
    broker=broker,
    backend=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    setup_defaults={"time_limit": 120, "soft_time_limit": 120},
)
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
