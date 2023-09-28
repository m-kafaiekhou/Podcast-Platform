from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

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
    queryset = PodcastEpisode.objects.get_active_list()
    pagination_class = CustomPagination


class PodcastEpisodeDetailView(generics.RetrieveAPIView):
    queryset = PodcastEpisode.objects.get_active_list()
    serializer_class = PodcastEpisodeSerializer
    lookup_field = 'pk'
