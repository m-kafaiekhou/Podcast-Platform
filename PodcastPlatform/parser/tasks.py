from celery import shared_task
from celery.exceptions import Retry
import random

from parser.parsers import PodcastRSSParser
from podcast.models import Podcast, PodcastEpisode


# def exponential_backoff(task):
#     retries = task.request.retries
#     backoff = 2 ** retries
#     rand = random.randint(1, 5)
#     return int(backoff + rand)


@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 5}, task_time_limit=600, retry_backoff=2)
def parse_feeds_to_db(self, podcast_pk):
    try:
        podcast_obj = Podcast.objects.get(pk=podcast_pk)
        parser = PodcastRSSParser(podcast_obj, PodcastEpisode)
        parser.fill_db()
    except Exception as e:
        raise e


@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 5}, task_time_limit=600, retry_backoff=2)
def podcast_parse_task(self):
    try:
        podcasts = Podcast.objects.all()

    except Exception as e:
        # NOTE log
        raise e

    for podcast in podcasts:
        parse_feeds_to_db.delay(podcast.pk)


