from django.contrib.contenttypes.models import ContentType
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from ...profiles.serializers.profiles import ProfileListSerializer
from ...profiles.services import get_profile
from ..models import Chat, Elected, ElectedMessage, Message


class ChatMessageSerializer(serializers.ModelSerializer):
    maker = serializers.SerializerMethodField()

    @staticmethod
    @extend_schema_field(ProfileListSerializer)
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
    @extend_schema_field(ChatMessageSerializer(allow_null=True, many=True))
    def get_messages(instance: Chat):
        return ChatMessageSerializer(Message.objects.filter(chat_id=instance.pk), many=True).data

    class Meta:
        model = Chat
        fields = ("messages",)


class ForwardElectedMessageSerializer(serializers.Serializer):
    message_id = serializers.IntegerField()

    def create(self, validated_data):
        message = get_object_or_404(Message, pk=validated_data["message_id"])
        elected = get_object_or_404(Elected, creator=get_profile(user=self.context.get("request").user))
        elected.electedmessage_set.add(ElectedMessage.objects.create(message=message, elected=elected))
        return message

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
