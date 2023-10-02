from rest_framework import serializers
from podcast.models import Podcast


class RSSLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcast
        fields = ('rss_url', )
