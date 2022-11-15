from django.db.models import Q
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Chat, Elected, Message, PrivateChat
from .serializers.chats import (
    ChatCreateSerializer,
    ChatListSerializer,
    ChatMediaCreateSerializer,
    ChatMemberSerializer,
    ChatRetrieveSerializer,
    PrivateChatCreateSerializer,
    PrivateChatSerializer,
)
from .serializers.messages import (
    ChatMessageCreateSerializer,
    ChatMessageListSerializer,
    ChatMessageSerializer,
    ChatMessageUpdateSerializer,
    ForwardElectedMessageSerializer,
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

    @action(methods=["GET"], detail=False)
    def elected(self, request: Request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(methods=["POST"], detail=False, url_path="elected/messages")
    def add_elected_message(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    @action(methods=["GET"], detail=True)
    def members(self, request, pk, *args, **kwargs):
        return Response(self.get_serializer(self.get_object()).data)

    @action(methods=["GET"], detail=True)
    def messages(self, request, pk, *args, **kwargs):
        return Response(self.get_serializer(self.get_object()).data)

    @action(methods=["POST"], detail=True)
    def medias(self, request, pk, *args, **kwargs):
        return super().create(request)

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
            case "medias":
                return ChatMediaCreateSerializer
            case "elected":
                return ChatMessageSerializer
            case "add_elected_message":
                return ForwardElectedMessageSerializer
            case _:
                return self.serializer_class

    def get_queryset(self):
        match self.action:
            case "list":
                return Chat.objects.filter(members__user=self.request.user)
            case "elected":
                return Elected.objects.get(creator__user=self.request.user).messages.all()
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


class PrivateChatViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    serializer_class = PrivateChatSerializer
    queryset = PrivateChat.objects.all()

    @action(methods=["GET"], detail=True)
    def messages(self, request, pk, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        match self.action:
            case "create":
                return PrivateChatCreateSerializer
            case "messages":
                return ChatMessageListSerializer
            case _:
                return self.serializer_class

    def get_queryset(self):
        match self.action:
            case "messages":
                pk = self.kwargs.get("pk")
                private_chat = get_object_or_404(self.queryset, pk=pk)
                return [private_chat]
            case _:
                return PrivateChat.objects.filter(
                    Q(first_member__user=self.request.user) | Q(second_member__user=self.request.user)
                )
