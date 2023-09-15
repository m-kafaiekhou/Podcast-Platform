from rest_framework import serializers
from .models import Podcast, PodcastEpisode


class PodcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcast
        fields = [
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

