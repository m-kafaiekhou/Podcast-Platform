from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.db.models.aggregates import Count


from .models import Podcast, PodcastEpisode
from .serializers import PodcastSerializer, PodcastEpisodeSerializer
from accounts.authentications import JWTAuthentication


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


class GetRecommendationsView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PodcastSerializer
    pagination_class = CustomPagination


    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            self.queryset = self.get_podcast_based_on_likes(user)
        else:
            self.queryset = Podcast.objects.annotate(num_likes=Count('podcastepisode__like')).order_by('-num_likes')
        
        return super().get_queryset()

    def get_podcast_based_on_likes(self, user):
        podcasts = Podcast.objects.all()
        podcast_episodes = PodcastEpisode.objects.select_related("podcast__category").prefetch_related('like').filter(like__user=user)
        
        rate_dict = {}

        for ep in podcast_episodes:
            category = ep.podcast.category
            rate_dict.setdefault(category, 0)
            rate_dict[category] += 1

        sorted_rate = [k for k,_ in sorted(rate_dict.items(), key=lambda item:item[1], reverse=True)]

        categories = sorted_rate[:4] if len(sorted_rate) > 4 else sorted_rate

        qs = podcasts.filter(category__in=categories)

        return qs
    