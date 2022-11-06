from typing import TypeVar

from rest_framework import serializers

from ..models import Comment

CommentSerializerT = TypeVar("CommentSerializerT", bound=serializers.ModelSerializer)


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("content",)
