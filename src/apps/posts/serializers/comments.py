from typing import TypeVar

from rest_framework import serializers

from ...profiles.services import get_profile
from ..models import Comment

CommentSerializerT = TypeVar("CommentSerializerT", bound=serializers.ModelSerializer)


class CommentCreateSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "creator", "post", "content", "answer")

    def create(self, validated_data):
        validated_data["creator"] = get_profile(user=self.context.get("request").user)
        return super().create(validated_data)


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("content",)
