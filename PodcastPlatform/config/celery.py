import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery("config")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'podcast-parse-task': {
        'task': 'parser.tasks.podcast_parse_task',
        # 'schedule': crontab(hour=23, minute=30), # ~3:00 AM Tehran
        'schedule': crontab(minute="*/1"),
    },
}

# task_annotations = {'*': {'rate_limit': '1/m'}}
# app.conf.task_default_rate_limit = '1/m'
