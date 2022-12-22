from typing import TypeVar

from rest_framework import serializers

from apps.profiles.services import get_profile

from ..models import Post, PostMedia, PostsGroup

PostSerializeT = TypeVar("PostSerializeT", bound=serializers.ModelSerializer)


class PostGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostsGroup
        fields = "__all__"


class PostGroupRetrieveSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()

    @staticmethod
    def get_posts(instance: PostsGroup):
        from ...profiles.serializers.profiles import FeedPostListSerializer

        return FeedPostListSerializer(instance.posts, many=True).data

    class Meta:
        model = PostsGroup
        fields = ("id", "title", "posts")


class PostMediaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMedia
        fields = "__all__"


class PostCreateSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ("description", "medias", "is_active", "creator")

    def create(self, validated_data):
        validated_data["creator"] = get_profile(user=self.context.get("request").user)
        result = super().create(validated_data)
        return result


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "medias")
        depth = 1


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        depth = 1


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ("creator", "medias")
