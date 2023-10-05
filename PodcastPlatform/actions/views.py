from rest_framework.views import APIView

from .mixins import InteractionMixin
from .models import Like, Comment, Bookmark, Subscription
from .serializers import CommentSerializer
from podcast.models import Podcast

class LikeView(InteractionMixin, APIView):
    model = Like


class SubscriptionView(InteractionMixin, APIView):
    action_model = Subscription
    model = Podcast


class CommentView(InteractionMixin, APIView):
    action_model = Comment
    model = Podcast

    serializer_class = CommentSerializer


    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        kwargs['content'] = serializer.validated_data['content']

        return super().post(request, **kwargs)


