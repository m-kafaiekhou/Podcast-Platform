from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import serializers

from .models import Podcast, PodcastEpisode
from .serializers import PodcastSerializer, PodcastEpisodeSerializer


class CustomPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = "page_size"
    max_page_size = 100


class PodcastListView(generics.ListAPIView):
    serializer_class = PodcastSerializer
    queryset = Podcast.objects.get_active_list()
    pagination_class = CustomPagination


class PodcastEpisodeListView(generics.ListAPIView):
    serializer_class = PodcastEpisodeSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        podcast_id = self.kwargs['podcast_id']
        self.queryset = PodcastEpisode.objects.filter(podcast_id=podcast_id, is_deleted=False)
        return super().get_queryset()


class PodcastEpisodeDetailView(generics.RetrieveAPIView):
    queryset = PodcastEpisode.objects.get_active_list()
    serializer_class = PodcastEpisodeSerializer
    lookup_field = 'pk'
