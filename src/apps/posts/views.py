from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from common.openapi import common_responses_schema

from .models import Comment, Post
from .serializers.comments import CommentCreateSerializer, CommentSerializerT, CommentUpdateSerializer
from .serializers.posts import (
    PostCreateSerializer,
    PostMediaCreateSerializer,
    PostSerializer,
    PostSerializeT,
    PostUpdateSerializer,
)


class CommentViewSet(
    mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        methods=["POST"],
        request=CommentCreateSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=CommentCreateSerializer, description="Create a new post's comment"
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Bad request"),
            **common_responses_schema(),
        },
        # examples=[*common_responses_examples()]  # noqa: E501 Examples was defined in common_responses_schema
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        methods=["PUT"],
        request=CommentUpdateSerializer,
        responses={
            status.HTTP_200_OK: CommentCreateSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Bad request"),
            **common_responses_schema(),
        },
    )
    def update(self, request, *args, **kwargs) -> Response:
        return super().update(request, *args, **kwargs)

    @extend_schema(
        methods=["PATCH"],
        request=CommentUpdateSerializer,
        responses={
            status.HTTP_200_OK: CommentCreateSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Bad request"),
            **common_responses_schema(),
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(methods=["DELETE"], responses={**common_responses_schema(status_codes=[status.HTTP_204_NO_CONTENT])})
    def destroy(self, request, *args, **kwargs) -> Response:
        return super().destroy(request, *args, **kwargs)

    def get_serializer_class(self) -> type[CommentSerializerT]:
        match self.action:
            case "create":
                return CommentCreateSerializer
            case "update":
                return CommentUpdateSerializer
            case "partial_update":
                return CommentUpdateSerializer
            case _:
                return CommentCreateSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=["POST"], detail=False, url_path=r"medias")
    def create_post_media(self, request: Request) -> Response:
        return super().create(request)

    def get_serializer_class(self) -> type[PostSerializeT]:
        match self.action:
            case "create":
                return PostCreateSerializer
            case "update":
                return PostUpdateSerializer
            case "partial_update":
                return PostUpdateSerializer
            case "create_post_media":
                return PostMediaCreateSerializer
            case _:
                return PostSerializer
