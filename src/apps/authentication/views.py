from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegisterSerializer, SignInTokenSerializer


class SignInView(TokenObtainPairView):
    """SignInView with custom token claims"""

    serializer_class = SignInTokenSerializer


@extend_schema(request=RegisterSerializer, responses=RegisterSerializer)
@api_view(http_method_names=["POST"])
def register_view(request: Request) -> Response:
    """Register view"""
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
