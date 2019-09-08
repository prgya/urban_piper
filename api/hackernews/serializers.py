
from rest_framework import serializers
from .models import hackernews


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = hackernews
        fields = ("story_id", "username", "title", "sentiment", "url", "upvotes")