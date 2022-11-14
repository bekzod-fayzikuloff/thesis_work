from rest_framework import serializers

from ...profiles.serializers.profiles import ProfileListSerializer
from ..models import Chat, Media


class ChatListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        exclude = ("members", "created_at", "updated_at")


class ChatCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        exclude = ("members",)


class ChatRetrieveSerializer(serializers.ModelSerializer):
    members_quantity = serializers.SerializerMethodField()

    @staticmethod
    def get_members_quantity(instance: Chat):
        return instance.members.count()

    class Meta:
        model = Chat
        fields = ("id", "title", "description", "members_quantity")


class ChatMemberSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()

    @staticmethod
    def get_members(instance: Chat):
        return ProfileListSerializer(instance.members, many=True).data

    class Meta:
        model = Chat
        fields = ("members",)


class ChatMediaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = "__all__"
