"""
Serializer for Post API
"""
from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    """Serializer class"""
    author_name = serializers.CharField(
        source="author.first_name", read_only=True
        )

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "body",
            "author_name"
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        """Create and return a user with encrypted password."""

        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["author"] = request.user
        return super().create(validated_data)
