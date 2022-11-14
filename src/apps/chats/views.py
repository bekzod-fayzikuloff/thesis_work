from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Chat, Message
from .serializers.chats import ChatCreateSerializer, ChatListSerializer, ChatMemberSerializer, ChatRetrieveSerializer
from .serializers.messages import (
    ChatMessageCreateSerializer,
    ChatMessageListSerializer,
    ChatMessageSerializer,
    ChatMessageUpdateSerializer,
)


class ChatViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):

    serializer_class = ChatListSerializer
    queryset = Chat.objects.all()

    @action(methods=["GET"], detail=True)
    def members(self, request, pk, *args, **kwargs):
        return Response(self.get_serializer(self.get_object()).data)

    @action(methods=["GET"], detail=True)
    def messages(self, request, pk, *args, **kwargs):
        return Response(self.get_serializer(self.get_object()).data)

    def get_serializer_class(self):
        match self.action:
            case "list":
                return ChatListSerializer
            case "create":
                return ChatCreateSerializer
            case "retrieve":
                return ChatRetrieveSerializer
            case "members":
                return ChatMemberSerializer
            case "messages":
                return ChatMessageListSerializer
            case _:
                return self.serializer_class

    def get_queryset(self):
        match self.action:
            case "list":
                return Chat.objects.filter(members__user=self.request.user)
            case _:
                return super().get_queryset()


class MessageViewSet(
    mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    serializer_class = ChatMessageSerializer
    queryset = Message.objects.all()

    def get_serializer_class(self):
        match self.action:
            case "create":
                return ChatMessageCreateSerializer
            case "update":
                return ChatMessageUpdateSerializer
            case "partial_update":
                return ChatMessageUpdateSerializer
            case _:
                return self.serializer_class
