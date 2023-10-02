from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status

from podcast.models import Podcast
from .serializers import RSSLinkSerializer
from accounts.authentications import JWTAuthentication
from .tasks import parse_feeds_to_db, podcast_parse_task


class ParseView(views.APIView):
    permission_classes = (IsAuthenticated, IsAdminUser, )
    authentication_classes = (JWTAuthentication, )
    serializer_class = RSSLinkSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=False)

        if valid:
            podcast = Podcast.objects.get_or_create(rss_url=serializer.data.get('rss_url'))
            parse_feeds_to_db.delay(podcast[0].id)

            return Response(
                data={"message": "Podcast related to your url has been updated/added"},
                status=status.HTTP_201_CREATED
            )
        podcast_parse_task.delay()

        return Response(
            data={"message": "All podcasts have been updated"},
            status=status.HTTP_201_CREATED
        )





