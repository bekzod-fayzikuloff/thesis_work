from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.authentication.models import User
from common.models import BaseModel


class Profile(BaseModel):
    """Описание таблицы профиля"""

    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, max_length=1000)

    def __str__(self) -> str:
        return f"{self.user.username}"

    class Meta:
        """Metaclass with table representation info."""

        ordering = ("-id",)
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"


class Follower(BaseModel):
    """Описание таблицы `фолловеров`"""

    follower = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name="followers")
    follow_to = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name="followed")

    def __str__(self) -> str:
        return f"{self.follower} follow to {self.follow_to}"

    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"
        unique_together = (("follower", "follow_to"),)
        constraints = [
            models.CheckConstraint(
                check=(~models.Q(follow_to=models.F("follower"))),
                name="check_follow_to_self",
                violation_error_message="Users cannot follow to themselves.",
            )
        ]


@receiver(post_save, sender=User)
def create_profile(sender, **kwargs) -> None:  # noqa
    if kwargs.get("created"):
        Profile.objects.create(user=kwargs.get("instance"))
