from django.contrib import admin
from .models import Podcast, PodcastEpisode

# Register your models here.


@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    search_fields = ['title', 'description', 'category', 'keywords']


@admin.register(PodcastEpisode)
class PodcastEpisodeAdmin(admin.ModelAdmin):
    search_fields = ['title', 'description', 'keywords']
    