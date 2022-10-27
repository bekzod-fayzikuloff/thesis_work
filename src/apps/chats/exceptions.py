from django.core.exceptions import ValidationError


class PrivateChatAlreadyExistsError(ValidationError):
    def __init__(self, message) -> None:
        super().__init__(message=message)
