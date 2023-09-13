from django.db import models



class PodcastFormat(models.Model):
    title = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)

    summary = models.CharField(max_length=100, null=True, blank=True)
    image = models.CharField(max_length=100, null=True, blank=True)
    host = models.CharField(max_length=100, null=True, blank=True)
    keywords = models.CharField(max_length=100, null=True, blank=True)
    explicit = models.CharField(max_length=100, null=True, blank=True)
    copyright = models.CharField(max_length=100, null=True, blank=True)
    language = models.CharField(max_length=100, null=True, blank=True)
    link = models.CharField(max_length=100, null=True, blank=True)
    
class PodcastEpisodeFormat(models.Model):
    audio_file_path = models.CharField(max_length=100)
    duration_path = models.CharField(max_length=100)
    title_path = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    audio_file = models.CharField(max_length=100)
    publish_date = models.CharField(max_length=100)

    explicit = models.CharField(max_length=100)
    summary = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    guests = models.CharField(max_length=100)
    keywords = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
