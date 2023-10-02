from rest_framework import serializers
from .models import Podcast, PodcastEpisode


class PodcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcast
        fields = [
            'id',
            "title",
            "description",
            "copyright",
            "generator",
            "link",
            "owner_name",
            "owner_email",
            "author",
            "summary",
            "language",
            "explicit",
            "category",
            "keywords",
            "icon_image_url",
            "image_url",
            "image_link",
            "image_title",
        ]


class PodcastEpisodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PodcastEpisode
        fields = [
            'id',
            "title",
            "description",
            "episode_num",
            "summary",
            "content",
            "guid",
            "publish_date",
            "explicit",
            "image_url",
            "keywords",
            "duration",
            "enclosure_url",
            "enclosure_type",
            "enclosure_length",
        ]
