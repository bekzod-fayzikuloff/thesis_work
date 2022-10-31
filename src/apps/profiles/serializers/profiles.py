from typing import TypeVar

from rest_framework import serializers

from ..models import Profile

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
    def get_username(instance):
        return instance.user.username

    class Meta:
        model = Profile
        fields = ("avatar", "username")


class ProfileUpdateSerializer(BaseProfileSerializer):
    class Meta:
        model = Profile
        exclude = ("user",)
