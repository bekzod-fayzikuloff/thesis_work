from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from common.openapi import common_responses_schema

from ..profiles.serializers.profiles import FeedPostListSerializer
from .filters import CommentFilter, PostFilter
from .models import Comment, Post, PostsGroup, Reaction
from .paginations import CommentResultsSetPagination
from .serializers.comments import (
    CommentCreateSerializer,
    CommentListSerializer,
    CommentSerializerT,
    CommentUpdateSerializer,
)
from .serializers.posts import (
    PostCreateSerializer,
    PostGroupRetrieveSerializer,
    PostGroupSerializer,
    PostListSerializer,
    PostMediaCreateSerializer,
    PostSerializer,
    PostSerializeT,
    PostUpdateSerializer,
    ReactionCreateSerializer,
)


class CommentViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = CommentFilter
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    pagination_class = CommentResultsSetPagination

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
    def create(self, request, *args, **kwargs) -> Response:
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
    def partial_update(self, request, *args, **kwargs) -> Response:
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
            case "list":
                return CommentListSerializer
            case _:
                return CommentCreateSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = PostFilter

    @action(methods=["POST"], detail=False, url_path=r"medias")
    def create_post_media(self, request: Request) -> Response:
        return super().create(request)

    def get_serializer_class(self) -> type[PostSerializeT]:
        match self.action:
            case "list":
                return PostListSerializer
            case "retrieve":
                return FeedPostListSerializer
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


class PostGroupViewSet(ModelViewSet):
    queryset = PostsGroup.objects.all()
    serializer_class = PostGroupSerializer

    @action(methods=["DELETE"], detail=True, url_path=r"posts-remove/(?P<post_pk>\d+)")
    def remove_post(self, request, *args, **kwargs):
        posts_group = get_object_or_404(PostsGroup, pk=kwargs.get("pk"))
        post = get_object_or_404(Post, pk=kwargs.get("post_pk"))
        posts_group.posts.remove(post)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        match self.action:
            case "retrieve":
                return PostGroupRetrieveSerializer
            case _:
                return PostGroupSerializer


class ReactionViewSet(ModelViewSet):
    queryset = Reaction.objects.all()
    serializer_class = ReactionCreateSerializer
