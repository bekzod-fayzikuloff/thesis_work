from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema_serializer
from rest_framework import serializers, status


def common_responses_schema(status_codes: list[int | str] = "__all__") -> dict[int, OpenApiResponse]:
    common_schemas = {
        status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
            response=UnAuthorizedRequestSerializer,
            description="Unauthorized",
            examples=[*common_responses_examples(status_codes=[status.HTTP_401_UNAUTHORIZED])],
        ),
        status.HTTP_404_NOT_FOUND: OpenApiResponse(
            response=NotFoundSerializer,
            description="Not Found",
            examples=[*common_responses_examples(status_codes=[status.HTTP_404_NOT_FOUND])],
        ),
        status.HTTP_204_NO_CONTENT: OpenApiResponse(
            description="No content", examples=[*common_responses_examples(status_codes=[status.HTTP_204_NO_CONTENT])]
        ),
    }
    if status_codes == "__all__":
        return common_schemas

    return {
        status_code: response_schema
        for status_code, response_schema in common_schemas.items()
        if status_code in [int(code) for code in status_codes]
    }


def common_responses_examples(status_codes: list[int | str] = "__all__") -> list[OpenApiExample]:
    common_examples = [
        OpenApiExample(
            "Not Found",
            description="Not Found",
            value={"detail": "Not found."},
            response_only=True,
            status_codes=[status.HTTP_404_NOT_FOUND],
        ),
        OpenApiExample(
            "Unauthorized",
            description="Unauthorized request",
            value={"detail": "Authentication credentials were not provided."},
            response_only=True,
            status_codes=[status.HTTP_401_UNAUTHORIZED],
        ),
        OpenApiExample(
            "No content",
            description="No content",
            value={},
            response_only=True,
            status_codes=[status.HTTP_204_NO_CONTENT],
        ),
    ]
    if status_codes == "__all__":
        return common_examples

    def _filter_by_status_code(api_example: OpenApiExample) -> bool:
        return any([str(code) in api_example.status_codes for code in status_codes])

    return list(filter(_filter_by_status_code, common_examples))


class ClientExceptionRequestSerializer(serializers.Serializer):
    detail = serializers.CharField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Error: Unauthorized",
            description="Request was made from a non-authorized user",
            value={"detail": "Authentication credentials were not provided."},
        ),
    ]
)
class UnAuthorizedRequestSerializer(ClientExceptionRequestSerializer):
    pass


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Not Found",
            description="Cannot find ",
            value=["Not found."],
        ),
    ]
)
class NotFoundSerializer(ClientExceptionRequestSerializer):
    pass
