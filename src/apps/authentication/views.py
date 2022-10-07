from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import UserSerializer


@extend_schema(request=UserSerializer, responses=UserSerializer)
@api_view(http_method_names=["POST"])
def register_view(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
