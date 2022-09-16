from rest_framework.decorators import api_view
from rest_framework.request import HttpRequest
from rest_framework.response import Response


@api_view(http_method_names=["GET"])
def index(request: HttpRequest) -> Response:
    return Response({"ping": "pong"})
