import abc
from typing import TypeVar

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from ...posts.models import Comment, Post, PostsGroup, Reaction
from ..models import Follower, Profile
from ..services import get_profile

ProfileSerializerType = TypeVar("ProfileSerializerType", bound="BaseProfileSerializer")


class BaseProfileSerializer(serializers.ModelSerializer):
    pass


class ProfileSerializer(BaseProfileSerializer):
    username = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    followed_to_count = serializers.SerializerMethodField()

    @staticmethod
    def get_username(instance: Profile):
        return instance.user.username

    @staticmethod
    def get_followers_count(instance: Profile):
        return Follower.objects.filter(follow_to=instance).count()

    @staticmethod
    def get_followed_to_count(instance: Profile):
        return Follower.objects.filter(follower=instance).count()

    @staticmethod
    def get_posts_count(instance: Profile):
        return Post.objects.filter(creator=instance).count()

    class Meta:
        model = Profile
        exclude = ("user",)


class ProfileListSerializer(BaseProfileSerializer):
    username = serializers.SerializerMethodField()

    @staticmethod
    @extend_schema_field(OpenApiTypes.STR)
    def get_username(instance: Profile):
        return instance.user.username

    class Meta:
        model = Profile
        fields = ("id", "avatar", "username")


class FollowerBaseListSerializer(BaseProfileSerializer):
    follower = serializers.SerializerMethodField()

    class Meta:
        model = Follower
        fields = ("id", "follower")

    @staticmethod
    @abc.abstractmethod
    def get_follower(instance: Follower):
        return ProfileListSerializer(instance.follower).data


class FeedPostListSerializer(BaseProfileSerializer):
    creator_username = serializers.SerializerMethodField()
    creator_id = serializers.SerializerMethodField()
    creator_avatar = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    post_is_liked = serializers.SerializerMethodField()
    post_is_saved = serializers.SerializerMethodField()
    comments_quantity = serializers.SerializerMethodField()

    @staticmethod
    def get_creator_username(instance: Post):
        return instance.creator.user.username

    @staticmethod
    def get_creator_id(instance: Post):
        return instance.creator.pk

    @staticmethod
    def get_creator_avatar(instance: Post):
        if not instance.creator.avatar:
            return None
        return instance.creator.avatar.url

    @staticmethod
    def get_likes(instance: Post):
        return Reaction.objects.filter(post=instance, is_active=True, is_positive=True).count()

    @staticmethod
    def get_comments_quantity(instance: Post):
        return Comment.objects.filter(post=instance).count()

    def get_post_is_saved(self, instance: Post):
        try:
            return bool(
                PostsGroup.objects.filter(creator=get_profile(user=self.context["request"].user), posts__in=[instance])
            )
        except KeyError:
            return False

    def get_post_is_liked(self, instance: Post):
        try:
            return bool(Reaction.objects.filter(post=instance, creator=get_profile(user=self.context["request"].user)))
        except KeyError:
            return False

    class Meta:
        model = Post
        exclude = ("creator",)
        depth = 1


class PostGroupSerializer(BaseProfileSerializer):
    class Meta:
        model = PostsGroup
        fields = "__all__"


class FollowerListSerializer(FollowerBaseListSerializer):
    @staticmethod
    def get_follower(instance: Follower):
        return ProfileListSerializer(instance.follower).data


class FollowedListSerializer(FollowerBaseListSerializer):
    @staticmethod
    def get_follower(instance: Follower):
        return ProfileListSerializer(instance.follow_to).data


class FollowerCreateSerializer(BaseProfileSerializer):
    follower = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Follower
        fields = ("id", "follow_to", "follower")

    def create(self, validated_data):
        validated_data["follower"] = get_profile(user=self.context["request"].user)
        return super().create(validated_data)


class ProfileUpdateSerializer(BaseProfileSerializer):
    class Meta:
        model = Profile
        exclude = ("user",)
