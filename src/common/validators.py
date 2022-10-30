from typing import Optional

from django.core.exceptions import ValidationError
from django.db.models.fields.files import FieldFile


def validate_file_size(value: FieldFile, max_size: int = 10485760) -> Optional[FieldFile]:
    if value.size > max_size:
        raise ValidationError(f"You cannot upload file more than {max_size / 1024 / 1024}Mb")
    else:
        return value
