from rest_framework import generics, views
from rest_framework.response import Response

from .models import Podcast, PodcastEpisode
from .serializers import PodcastSerializer, PodcastEpisodeSerializer


class PodcastListCreateView(generics.ListAPIView):
    serializer_class = PodcastSerializer
    queryset = Podcast.objects.get_active_list()


class PodcastEpisodeListCreateView(views.APIView):

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        podcast = Podcast.objects.get(pk=pk)
        episode_queryset = PodcastEpisode.objects.filter(podcast__id=pk, is_deleted=False)

        podcast_serializer = PodcastSerializer(podcast)
        episode_serializer = PodcastEpisodeSerializer(episode_queryset, many=True)

        data = {
            'podcast': podcast_serializer.data,
            'episodes': episode_serializer.data
            }
        
        return Response(data=data)
