from django.urls import path
from .views import (
        PodcastListView,
        PodcastEpisodeListView,
        PodcastEpisodeDetailView,
        GetRecommendationsView)

app_name = 'podcast'

urlpatterns =[
    path("", PodcastListView.as_view(), name="podcast-list"),
    path("episodes/<int:pk>/", PodcastEpisodeListView.as_view(), name="podcast-episode-list"),
    path("episode/detail/<int:pk>/", PodcastEpisodeDetailView.as_view(), name="podcast-episode-detail"),
    path("recommendations/", GetRecommendationsView.as_view(), name="recommendation"),

]
    