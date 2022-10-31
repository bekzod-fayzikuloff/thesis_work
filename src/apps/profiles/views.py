from typing import Type

from drf_spectacular.utils import extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Profile
from .serializers.profiles import (
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

    @extend_schema(responses={status.HTTP_200_OK: ProfileListSerializer}, methods=["GET"])
    def list(self, request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)

    @extend_schema(methods=["GET"])
    @action(methods=["GET"], detail=False, url_path=r"me")
    def profile_detail(self, request: Request) -> Response:
        instance = Profile.objects.get(user=self.request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @extend_schema(responses={status.HTTP_204_NO_CONTENT: None}, methods=["DELETE"])
    @action(methods=["DELETE"], detail=False, url_path=r"me/delete")
    def delete_profile(self, request: Request, *args, **kwargs) -> Response:
        instance = Profile.objects.get(user=self.request.user)
        self.perform_delete(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        request=ProfileUpdateSerializer,
        responses={
            status.HTTP_200_OK: ProfileSerializer,
            status.HTTP_404_NOT_FOUND: None,
            status.HTTP_403_FORBIDDEN: None,
        },
        methods=["PUT", "PATCH"],
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
            case _:
                return ProfileSerializer

    @staticmethod
    def perform_delete(instance: Profile) -> None:
        instance.user.delete()
        instance.delete()
