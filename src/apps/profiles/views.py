from typing import Type

from drf_spectacular.utils import extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from common.openapi import common_responses_schema

from .filters import FollowerFilter, ProfileFilter
from .models import Follower, Profile
from .serializers.profiles import (
    FollowerCreateSerializer,
    FollowerListSerializer,
    ProfileListSerializer,
    ProfileSerializer,
    ProfileSerializerType,
    ProfileUpdateSerializer,
)


class ProfileViewSet(
    mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]
    filterset_class = ProfileFilter

    @extend_schema(
        methods=["GET"],
        responses={
            status.HTTP_200_OK: ProfileListSerializer,
            **common_responses_schema(status_codes=[status.HTTP_401_UNAUTHORIZED]),
        },
    )
    def list(self, request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)

    @extend_schema(
        methods=["GET"],
        responses={
            status.HTTP_200_OK: ProfileSerializer,
            **common_responses_schema(status_codes=[status.HTTP_401_UNAUTHORIZED, status.HTTP_404_NOT_FOUND]),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        methods=["GET"],
        responses={
            status.HTTP_200_OK: FollowerListSerializer,
            **common_responses_schema(status_codes=[status.HTTP_401_UNAUTHORIZED]),
        },
    )
    @action(methods=["GET"], detail=True)
    def followers(self, request: Request, *args, **kwargs) -> Response:
        followers_qs = Follower.objects.filter(follow_to=self.get_object())
        return Response(data=self.get_serializer(followers_qs, many=True).data)

    @extend_schema(
        methods=["GET"],
        responses={
            status.HTTP_200_OK: FollowerListSerializer,
            **common_responses_schema(status_codes=[status.HTTP_401_UNAUTHORIZED]),
        },
    )
    @action(methods=["GET"], detail=True)
    def followed(self, request: Request, *args, **kwargs) -> Response:
        followed_qs = Follower.objects.filter(follower=self.get_object())
        return Response(data=self.get_serializer(followed_qs, many=True).data)

    @extend_schema(
        methods=["GET"],
        responses={
            status.HTTP_200_OK: ProfileSerializer,
            **common_responses_schema(status_codes=[status.HTTP_401_UNAUTHORIZED]),
        },
    )
    @action(methods=["GET"], detail=False, url_path=r"me")
    def profile_detail(self, request: Request) -> Response:
        instance = Profile.objects.get(user=self.request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @extend_schema(
        methods=["DELETE"],
        responses={**common_responses_schema(status_codes=[status.HTTP_204_NO_CONTENT, status.HTTP_401_UNAUTHORIZED])},
    )
    @action(methods=["DELETE"], detail=False, url_path=r"me/delete")
    def delete_profile(self, request: Request, *args, **kwargs) -> Response:
        instance = Profile.objects.get(user=self.request.user)
        self.perform_delete(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        methods=["PUT", "PATCH"],
        request=ProfileUpdateSerializer,
        responses={
            status.HTTP_200_OK: ProfileSerializer,
            status.HTTP_403_FORBIDDEN: None,
            **common_responses_schema(status_codes=[status.HTTP_401_UNAUTHORIZED, status.HTTP_404_NOT_FOUND]),
        },
    )
    def update(self, request: Request, *args, **kwargs) -> Response:
        profile = get_object_or_404(Profile, user__id=kwargs.get("pk"))
        if profile != Profile.objects.get(user=self.request.user):
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def get_serializer_class(self) -> Type[ProfileSerializerType]:
        match self.action:
            case "list":
                return ProfileListSerializer
            case "update_profile":
                return ProfileUpdateSerializer
            case "followers":
                return FollowerListSerializer
            case "followed":
                return FollowerListSerializer
            case _:
                return ProfileSerializer

    @staticmethod
    def perform_delete(instance: Profile) -> None:
        instance.user.delete()
        instance.delete()

    def get_object(self) -> Profile:
        return super().get_object()


class FollowerViewSet(mixins.DestroyModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Follower.objects.all()
    serializer_class = FollowerCreateSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = FollowerFilter

    @extend_schema(
        methods=["POST"],
        request=FollowerCreateSerializer,
        responses={
            status.HTTP_201_CREATED: FollowerCreateSerializer,
            **common_responses_schema(status_codes=[status.HTTP_401_UNAUTHORIZED, status.HTTP_400_BAD_REQUEST]),
        },
    )
    def create(self, request, *args, **kwargs) -> Response:
        return super().create(request, *args, **kwargs)

    @extend_schema(
        methods=["DELETE"],
        responses={**common_responses_schema(status_codes=[status.HTTP_401_UNAUTHORIZED, status.HTTP_204_NO_CONTENT])},
    )
    def destroy(self, request, *args, **kwargs) -> Response:
        return super().destroy(request, *args, **kwargs)
