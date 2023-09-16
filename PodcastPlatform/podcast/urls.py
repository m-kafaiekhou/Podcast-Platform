from django.urls import path
from .views import PodcastListView, PodcastEpisodeListView, PodcastEpisodeDetailView

app_name = 'podcast'

urlpatterns =[
    path("podcasts/", PodcastListView.as_view(), name="podcast-list"),
    path("podcasts/episodes/<int:pk>/", PodcastEpisodeListView.as_view(), name="podcast-episode-list"),
    path("podcasts/episode/detail/<int:pk>/", PodcastEpisodeDetailView.as_view(), name="podcast-episode-detail"),
]
    