from django.contrib import admin
from .models import Podcast, PodcastEpisode

# Register your models here.


@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    pass


@admin.register(PodcastEpisode)
class PodcastEpisodeAdmin(admin.ModelAdmin):
    pass