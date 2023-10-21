from celery import chain, shared_task, Task, group
from celery.exceptions import Retry
import logging
from elasticsearch import Elasticsearch
from django.conf import settings
from datetime import datetime

from parser.parsers import PodcastRSSParser
from podcast.models import Podcast, PodcastEpisode


logger = logging.getLogger('celery-log')  # TODO : __name__


def divide_tasks(tasks, div):
    groups = [group(tasks[i:i+div]) for i in range(0, len(tasks), div)]

    return groups

    
class CustomBaseTask(Task):
    autoretry_for = (Exception,)
    retry_kwargs = {'max_retries': 5}
    retry_backoff = 2
    retry_jitter=True
    task_time_limit=600

    es = Elasticsearch('http://elastic:9200')

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        # super().on_retry(exc=exc, task_id=task_id, *args, **kwargs)
        job = self.job if hasattr(self, 'job') else 'update'
        message = f'rerunning Task {self.name}'
        doc = {'timestamp': datetime.now().strftime("%Y-%m-%dT%H:%M"), 'task_id': task_id, 'task_name': self.name, 'exc': einfo, 'message': message, 'status': 'retry', 'event': f'celery_task_{job}_retry'}
        self.es.index(index=f'{settings.CELERY_LOG_INDEX_PREFIX}_{datetime.now().strftime("%Y-%m-%d")}', body=doc)
        # logger.warning(message)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # super().on_failure(exc=exc, task_id=task_id, *args, **kwargs)
        job = self.job if hasattr(self, 'job') else 'update'
        message = f'Task {self.name} failed'
        doc = {'timestamp': datetime.now().strftime("%Y-%m-%dT%H:%M"), 'task_id': task_id, 'task_name': self.name, 'exc': str(einfo), 'message': message, 'status': 'failure', 'event': f'celery_task_{job}_failure'}
        self.es.index(index=f'{settings.CELERY_LOG_INDEX_PREFIX}_{datetime.now().strftime("%Y-%m-%d")}', body=doc)
        # logger.critical(message)

    def on_success(self, retval, task_id, args, kwargs):
        # super().on_success(retval=retval, task_id=task_id, *args, **kwargs)
        job = self.job if hasattr(self, 'job') else 'update'
        message = f'Task {self.name} ran successfully'
        doc = {'timestamp': datetime.now().strftime("%Y-%m-%dT%H:%M"), 'task_id': task_id, 'task_name': self.name, 'message': message, 'status': 'success', 'event': f'celery_task_{job}_success'}
        self.es.index(index=f'{settings.CELERY_LOG_INDEX_PREFIX}_{datetime.now().strftime("%Y-%m-%d")}', body=doc)
        # logger.info(message)


@shared_task(base=CustomBaseTask, bind=True)
def parse_feeds_to_db(self, podcast_pk, job="update"):
    print('second' * 30)
    self.job = job
    podcast_obj = Podcast.objects.get(pk=podcast_pk)
    parser = PodcastRSSParser(podcast_obj, PodcastEpisode)
    parser.execute()


@shared_task(base=CustomBaseTask, bind=True)
def podcast_parse_task(self):
    print('main' * 30)
    podcasts = Podcast.objects.all()

    tasks = [parse_feeds_to_db.si(podcast_pk=podcast.pk) for podcast in podcasts]
    task_groups = divide_tasks(tasks, settings.CHUNK_SIZE)

    initial_chain = chain()
    for task_group in task_groups:
        initial_chain = initial_chain | task_group

    initial_chain.apply_async()

