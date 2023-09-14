from django.db import models

from parser.parsers import PodcastRSSParser
from core.models import BaseModel


class Podcast(BaseModel):
    rss_url = models.CharField(max_length=200)

    # episode_format = models.ForeignKey(PodcastEpisodeFormat, on_delete=models.PROTECT)
    # podcast_format = models.ForeignKey(PodcastFormat, on_delete=models.PROTECT)
 
    title = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    copyright = models.CharField(max_length=256, null=True, blank=True)
    generator = models.CharField(max_length=256, null=True, blank=True)
    link = models.CharField(max_length=512, null=True, blank=True)
    owner_name = models.CharField(max_length=256, null=True, blank=True)
    owner_email = models.CharField(max_length=256, null=True, blank=True)
    author = models.CharField(max_length=256, null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=256, null=True, blank=True)
    explicit = models.CharField(max_length=256, null=True, blank=True)
    category = models.CharField(max_length=256, null=True, blank=True)
    keywords = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=256, null=True, blank=True)
    icon_image_url = models.CharField(max_length=512, null=True, blank=True)
    image_url = models.CharField(max_length=512, null=True, blank=True)
    image_link = models.CharField(max_length=256, null=True, blank=True)
    image_title = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.title or super().__str__()
    


class PodcastEpisode(BaseModel):
    podcast = models.ForeignKey(Podcast, on_delete=models.PROTECT)

    title = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    episode_num = models.CharField(max_length=256, null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    guid = models.CharField(max_length=256, null=True, blank=True, unique=True)
    publish_date = models.CharField(max_length=256, null=True, blank=True)
    explicit = models.CharField(max_length=256, null=True, blank=True)
    image_url = models.CharField(max_length=512, null=True, blank=True)
    keywords = models.TextField(null=True, blank=True)
    duration = models.CharField(max_length=256, null=True, blank=True)
    enclosure_url = models.CharField(max_length=512, null=True, blank=True)
    enclosure_type = models.CharField(max_length=256, null=True, blank=True)
    enclosure_length = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self) -> str:
        return self.title

# Podcast.objects.bulk_create(ignore_conflicts==True)