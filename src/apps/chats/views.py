from django.db.models import Q
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from common.openapi import common_responses_schema

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
    permission_classes = [IsAuthenticated]

    @extend_schema(
        methods=["GET"],
        responses={
            status.HTTP_200_OK: OpenApiResponse(response=ChatListSerializer),
            **common_responses_schema(status_codes=[status.HTTP_401_UNAUTHORIZED]),
        },
    )
    def list(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)

    @extend_schema(
        methods=["POST"],
        request=ChatCreateSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(response=ChatCreateSerializer, description="Create a new chat"),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Bad request"),
            **common_responses_schema(status_codes=[status.HTTP_401_UNAUTHORIZED]),
        },
    )
    def create(self, request: Request, *args, **kwargs) -> Response:
        return super().create(request, *args, **kwargs)

    @extend_schema(
        methods=["GET"],
        responses={
            status.HTTP_200_OK: OpenApiResponse(response=ChatRetrieveSerializer, description="Get a chat object data"),
            **common_responses_schema(status_codes=[status.HTTP_401_UNAUTHORIZED, status.HTTP_404_NOT_FOUND]),
        },
    )
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        methods=["PUT"],
        responses={
            status.HTTP_200_OK: OpenApiResponse(response=ChatListSerializer, description="Update a chat data"),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Bad request"),
            **common_responses_schema(status_codes=[status.HTTP_401_UNAUTHORIZED, status.HTTP_404_NOT_FOUND]),
        },
    )
    def update(self, request: Request, *args, **kwargs) -> Response:
        return super().update(request, *args, **kwargs)

    @extend_schema(
        methods=["GET"],
        responses={
            status.HTTP_200_OK: OpenApiResponse(response=ChatListSerializer, description="Update a chat data"),
            **common_responses_schema(status_codes=[status.HTTP_401_UNAUTHORIZED, status.HTTP_404_NOT_FOUND]),
        },
    )
    @action(methods=["GET"], detail=False)
    def elected(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)

    @extend_schema(
        methods=["POST"],
        request=ForwardElectedMessageSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(response=ChatListSerializer, description="Update a chat data"),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Bad request"),
            **common_responses_schema(status_codes=[status.HTTP_401_UNAUTHORIZED, status.HTTP_404_NOT_FOUND]),
        },
    )
    @action(methods=["POST"], detail=False, url_path="elected/messages")
    def add_elected_message(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    @extend_schema(
        methods=["GET"],
        responses={
            status.HTTP_200_OK: ChatMemberSerializer,
            **common_responses_schema(status_codes=[status.HTTP_401_UNAUTHORIZED]),
        },
    )
    @action(methods=["GET"], detail=True)
    def members(self, request, *args, **kwargs) -> Response:
        return Response(self.get_serializer(self.get_object()).data)

    @extend_schema(
        methods=["GET"],
        responses={
            status.HTTP_200_OK: ChatMessageListSerializer,
            **common_responses_schema(status_codes=[status.HTTP_401_UNAUTHORIZED]),
        },
    )
    @action(methods=["GET"], detail=True)
    def messages(self, request, *args, **kwargs) -> Response:
        return Response(self.get_serializer(self.get_object()).data)

    @extend_schema(
        methods=["POST"],
        request=ChatMediaCreateSerializer,
        responses={
            status.HTTP_201_CREATED: ChatMediaCreateSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Bad request"),
            **common_responses_schema(status_codes=[status.HTTP_401_UNAUTHORIZED]),
        },
    )
    @action(methods=["POST"], detail=True)
    def medias(self, request, *args, **kwargs) -> Response:
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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

    @action(methods=["GET"], detail=True)
    def messages(self, request, *args, **kwargs) -> Response:
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
