from rest_framework import serializers

from ...profiles.serializers.profiles import ProfileListSerializer
from ...profiles.services import get_profile
from ..models import Chat, Media, PrivateChat


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


class PrivateChatCreateSerializer(serializers.ModelSerializer):
    first_member = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = PrivateChat
        fields = ("first_member", "second_member")

    def create(self, validated_data):
        validated_data["first_member"] = get_profile(user=self.context.get("request").user)
        result = super().create(validated_data)
        return result


class PrivateChatSerializer(serializers.ModelSerializer):
    member = serializers.SerializerMethodField()

    def get_member(self, instance: PrivateChat):
        if instance.first_member == get_profile(user=self.context.get("request").user):
            return ProfileListSerializer(instance.second_member).data
        return ProfileListSerializer(instance.first_member).data

    class Meta:
        model = PrivateChat
        exclude = ("first_member", "second_member")
