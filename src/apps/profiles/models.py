from django.db import models

from apps.authentication.models import User
from common.models import BaseModel


class Profile(BaseModel):
    """Profile model"""

    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, max_length=1000)

    def __str__(self) -> str:
        return f"{self.user.username}"

    class Meta:
        """Metaclass with table representation info."""

        verbose_name = "Profile"
        verbose_name_plural = "Profiles"


class Follower(BaseModel):
    """Follower model"""

    follower = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name="followers")
    follow_to = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name="followed")

    def __str__(self) -> str:
        return f"{self.follower} follow to {self.follow_to}"

    class Meta:
        """Metaclass with table constraints and table representation info."""

        verbose_name = "Follower"
        verbose_name_plural = "Followers"
        unique_together = (("follower", "follow_to"),)
        constraints = [
            models.CheckConstraint(
                check=(~models.Q(follow_to=models.F("follower"))),
                name="check_follow_to_self",
                violation_error_message="User cannot follow to self",
            )
        ]
