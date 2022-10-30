from rest_framework import mixins, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Profile
from .serializers.profiles import ProfileSerializer


@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated])
def index(request: Request):
    return Response("Its response")


class ProfileViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
