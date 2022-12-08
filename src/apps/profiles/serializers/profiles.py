from typing import TypeVar

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from ...posts.models import Post
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


class FollowerListSerializer(BaseProfileSerializer):
    follower = serializers.SerializerMethodField()

    class Meta:
        model = Follower
        fields = ("id", "follower")

    @staticmethod
    @extend_schema_field(ProfileListSerializer)
    def get_follower(instance: Follower):
        return ProfileListSerializer(instance.follower).data


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
