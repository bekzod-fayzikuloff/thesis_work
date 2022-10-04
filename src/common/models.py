from dirtyfields import DirtyFieldsMixin
from django.db import models


class BaseModel(DirtyFieldsMixin, models.Model):
    """BaseModel"""

    id = models.BigAutoField(primary_key=True, verbose_name="ID записи")

    created_at = models.DateTimeField("Время создания записи", db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField("Время изменения записи", db_index=True, auto_now=True)

    class Meta:
        abstract = True

    @property
    def dirty_fields(self) -> dict:
        """Getting changed still uncommited fields"""
        return self.get_dirty_fields(check_relationship=True)
