from django.db import models
from core.models import BaseModel


# class PodcastFormat(BaseModel):
#     title = models.CharField(max_length=100, null=True, blank=True)
#     description = models.CharField(max_length=100, null=True, blank=True)
#     copyright = models.CharField(max_length=100, null=True, blank=True)
#     generator = models.CharField(max_length=100, null=True, blank=True)
#     link = models.CharField(max_length=100, null=True, blank=True)
#     owner_name = models.CharField(max_length=100, null=True, blank=True)
#     owner_email = models.CharField(max_length=100, null=True, blank=True)
#     author = models.CharField(max_length=100, null=True, blank=True)
#     summary = models.CharField(max_length=100, null=True, blank=True)
#     language = models.CharField(max_length=100, null=True, blank=True)
#     explicit = models.CharField(max_length=100, null=True, blank=True)
#     category = models.CharField(max_length=100, null=True, blank=True)
#     keywords = models.CharField(max_length=100, null=True, blank=True)
#     type = models.CharField(max_length=100, null=True, blank=True)
#     icon_image_url = models.CharField(max_length=100, null=True, blank=True)
#     image_url = models.CharField(max_length=100, null=True, blank=True)
#     image_link = models.CharField(max_length=100, null=True, blank=True)
#     image_title = models.CharField(max_length=100, null=True, blank=True)


# class PodcastEpisodeFormat(BaseModel):
#     title = models.CharField(max_length=100)
#     description = models.CharField(max_length=100)
#     episode_type = models.CharField(max_length=100)
#     episode_num = models.CharField(max_length=100)
#     summary = models.CharField(max_length=100)
#     content = models.CharField(max_length=100)
#     guid = models.CharField(max_length=100)
#     publish_date = models.CharField(max_length=100)
#     explicit = models.CharField(max_length=100)
#     image_url = models.CharField(max_length=100)
#     keywords = models.CharField(max_length=100)
#     duration = models.CharField(max_length=100)
#     enclosure_url = models.CharField(max_length=100)
#     enclosure_type = models.CharField(max_length=100)
#     enclosure_length = models.CharField(max_length=100)
