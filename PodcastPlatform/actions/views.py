from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from .mixins import InteractionMixin
from .models import Like, Comment, Bookmark, Subscription
from .serializers import CommentSerializer
from podcast.models import Podcast, PodcastEpisode


class LikeView(InteractionMixin, APIView):
    action_model = Like
    model = PodcastEpisode


class SubscriptionView(InteractionMixin, APIView):
    action_model = Subscription
    model = Podcast


class CommentView(InteractionMixin, APIView):
    action_model = Comment
    model = PodcastEpisode

    serializer_class = CommentSerializer


    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        kwargs['content'] = serializer.validated_data['content']

        return super().post(request, **kwargs)
    
    def put(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        content = serializer.validated_data['content']

        pk = request.data.get('pk')

        item = get_object_or_404(self.action_model, pk=pk)
        item.content = content
        item.save()

        return Response({'message': f"Your object has been updated successfully ."}, status=status.HTTP_204_NO_CONTENT)


class BookmarkView(InteractionMixin, APIView):
    action_model = Bookmark
    model = Podcast
