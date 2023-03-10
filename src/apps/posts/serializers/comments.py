from typing import TypeVar

from rest_framework import serializers

from ...profiles.services import get_profile
from ..models import Comment

CommentSerializerT = TypeVar("CommentSerializerT", bound=serializers.ModelSerializer)


class CommentListSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    creator_id = serializers.SerializerMethodField()

    @staticmethod
    def get_avatar(instance: Comment):
        if not instance.creator.avatar:
            return None
        return instance.creator.avatar.url

    @staticmethod
    def get_username(instance: Comment):
        return instance.creator.user.username

    @staticmethod
    def get_creator_id(instance: Comment):
        return instance.creator.pk

    class Meta:
        model = Comment
        fields = ("id", "content", "avatar", "username", "creator_id", "created_at", "updated_at")


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
