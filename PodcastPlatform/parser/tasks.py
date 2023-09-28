from celery import shared_task
from celery.exceptions import Retry
import random
import logging

from parser.parsers import PodcastRSSParser
from podcast.models import Podcast, PodcastEpisode


logger = logging.getLogger('celery-log')


@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 5}, retry_jitter=True, task_time_limit=600, retry_backoff=2)
def parse_feeds_to_db(self, podcast_pk):
    try:
        podcast_obj = Podcast.objects.get(pk=podcast_pk)
        parser = PodcastRSSParser(podcast_obj, PodcastEpisode)
        parser.fill_db()
    except Exception as e:
        retry_count = self.request.retries
        message = f"task parse_feeds_to_db failed for the {retry_count} time"

        if retry_count < 5:
            logger.error(message)
        else:
            logger.critical(message)
        raise e


@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 5}, retry_jitter=True, task_time_limit=600, retry_backoff=2)
def podcast_parse_task(self):
    try:
        podcasts = Podcast.objects.all()

    except Exception as e:
        retry_count = self.request.retries
        message = f"task podcast_parse_task failed for the {retry_count} time"

        if retry_count < 5:
            logger.error(message)
        else:
            logger.critical(message)
        raise e

    for podcast in podcasts:
        parse_feeds_to_db.delay(podcast.pk)


