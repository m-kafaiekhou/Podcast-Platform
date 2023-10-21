from django.urls import path
from .views import LikeView, CommentView, BookmarkView, SubscriptionView


app_name = 'actions'
urlpatterns = [
    path('like/', LikeView.as_view(), name='like'),
    path('comment/', CommentView.as_view(), name='comment'),
    path('bookmark/', BookmarkView.as_view(), name='bookmark'),
    path('subscription/', SubscriptionView.as_view(), name='subscription'),
]