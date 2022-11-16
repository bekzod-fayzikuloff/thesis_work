from typing import TypeVar

from rest_framework import serializers

from ..models import Follower, Profile
from ..services import get_profile

ProfileSerializerType = TypeVar("ProfileSerializerType", bound="BaseProfileSerializer")


class BaseProfileSerializer(serializers.ModelSerializer):
    pass


class ProfileSerializer(BaseProfileSerializer):
    class Meta:
        model = Profile
        exclude = ("user",)


class ProfileListSerializer(BaseProfileSerializer):
    username = serializers.SerializerMethodField()

    @staticmethod
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
