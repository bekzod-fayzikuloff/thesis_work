from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from ...profiles.serializers.profiles import ProfileListSerializer
from ...profiles.services import get_profile
from ..models import Chat, Message


class ChatMessageSerializer(serializers.ModelSerializer):
    maker = serializers.SerializerMethodField()

    @staticmethod
    def get_maker(instance: Message):
        return ProfileListSerializer(instance.maker).data

    class Meta:
        model = Message
        exclude = ("updated_at", "is_active", "chat_type")
        depth = 1


class ChatMessageCreateSerializer(serializers.ModelSerializer):
    maker = serializers.PrimaryKeyRelatedField(read_only=True)
    chat_type = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = "__all__"

    def create(self, validated_data):
        validated_data["maker"] = get_profile(user=self.context.get("request").user)
        validated_data["chat_type"] = ContentType.objects.get_for_model(Message)
        result = super().create(validated_data)
        return result


class ChatMessageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("content", "is_active", "answer")


class ChatMessageListSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()

    @staticmethod
    def get_messages(instance: Chat):
        return ChatMessageSerializer(Message.objects.filter(chat_id=instance.pk), many=True).data

    class Meta:
        model = Chat
        fields = ("messages",)
