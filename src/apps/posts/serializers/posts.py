from typing import TypeVar

from rest_framework import serializers

from apps.profiles.services import get_profile

from ..models import Comment, Post, PostMedia, PostsGroup, Reaction

PostSerializeT = TypeVar("PostSerializeT", bound=serializers.ModelSerializer)


class PostGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostsGroup
        fields = "__all__"

    def update(self, instance: PostsGroup, validated_data):
        for p in validated_data.get("posts"):
            instance.posts.add(p)
        instance.save()
        return instance


class PostGroupRetrieveSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()

    @staticmethod
    def get_posts(instance: PostsGroup):

        return PostListSerializer(instance.posts, many=True).data

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
    comments = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    @staticmethod
    def get_comments(instance: Post):
        return Comment.objects.filter(post=instance).count()

    @staticmethod
    def get_likes(instance: Post):
        return Reaction.objects.filter(post=instance, is_active=True, is_positive=True).count()

    class Meta:
        model = Post
        fields = ("id", "medias", "likes", "comments")
        depth = 1


class PostSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    @staticmethod
    def get_comments(instance: Post):
        return Comment.objects.filter(post=instance).count()

    @staticmethod
    def get_likes(instance: Post):
        return Reaction.objects.filter(post=instance, is_active=True, is_positive=True).count()

    class Meta:
        model = Post
        fields = "__all__"
        depth = 1


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ("creator", "medias")


class ReactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = "__all__"
