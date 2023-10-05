from rest_framework.views import APIView

from .mixins import InteractionMixin
from .models import Like, Comment, Bookmark, Subscription
from .serializers import CommentSerializer
from podcast.models import Podcast

class LikeView(InteractionMixin, APIView):
    model = Like


