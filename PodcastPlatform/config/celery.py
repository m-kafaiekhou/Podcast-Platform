import os
from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery("config")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.broker_transport_options = {"visibility_timeout": settings.MAX_TIMEOUT_IN_SECONDS}

app.autodiscover_tasks()


# task_annotations = {'*': {'rate_limit': '1/m'}}
# app.conf.task_default_rate_limit = '1/m'
