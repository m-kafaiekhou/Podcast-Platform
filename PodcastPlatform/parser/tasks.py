from celery import shared_task, Task
from celery.exceptions import Retry
import logging
from elasticsearch import Elasticsearch

from parser.parsers import PodcastRSSParser
from podcast.models import Podcast, PodcastEpisode


logger = logging.getLogger('celery-log')  # TODO : __name__


class CustomBaseTask(Task):
    autoretry_for = (Exception,)
    retry_kwargs = {'max_retries': 5}
    retry_backoff = 2
    retry_jitter=True
    task_time_limit=600

    es = Elasticsearch()

    def on_retry(self, exc, task_id, args, kwargs):
        super().on_retry(exc=exc, task_id=task_id, *args, **kwargs)
        message = f'rerunning Task {self.name}'
        doc = {'task_id': task_id, 'task_name': self.name, 'message': message, 'status': 'retry'}
        self.es.index(index='task_logs', body=doc)

    def on_failure(self, exc, task_id, *args, **kwargs):
        super().on_failure(exc=exc, task_id=task_id, *args, **kwargs)
        message = f'Task {self.name} failed'
        doc = {'task_id': task_id, 'task_name': self.name, 'message': message, 'status': 'failure'}
        self.es.index(index='task_logs', body=doc)

    def on_success(self, retval, task_id, *args, **kwargs):
        super().on_success(retval=retval, task_id=task_id, *args, **kwargs)
        message = f'Task {self.name} ran successfully'
        doc = {'task_id': task_id, 'task_name': self.name, 'message': message, 'status': 'success'}
        self.es.index(index='task_logs', body=doc)


@shared_task(base=CustomBaseTask, bind=True)
def parse_feeds_to_db(self, podcast_pk):
    # try:
        # retry_count = self.request.retries
        # message = f"running task parse_feeds_to_db for the {retry_count} time"
        # logger.info(message)

    podcast_obj = Podcast.objects.get(pk=podcast_pk)
    parser = PodcastRSSParser(podcast_obj, PodcastEpisode)
    parser.execute()

        # message = f"ran task parse_feeds_to_db for the {retry_count} time"
        # logger.info(message)
    # except Exception as e:
        # retry_count = self.request.retries
        # message = f"task parse_feeds_to_db failed for the {retry_count} time"

        # if retry_count < 5:
        #     logger.error(message)
        # else:
        #     logger.critical(message)
        # raise e


@shared_task(base=CustomBaseTask, bind=True)
def podcast_parse_task(self):
    podcasts = Podcast.objects.all()

    for podcast in podcasts:
        parse_feeds_to_db.delay(podcast.pk)


