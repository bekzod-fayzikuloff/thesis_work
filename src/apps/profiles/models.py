import random

from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.authentication.models import User
from common.models import BaseModel


class Profile(BaseModel):
    """Profile model definition"""

    avatar = models.ImageField(upload_to="profiles/media/%Y/%m/%d/", blank=True, null=True)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, max_length=1000)
    is_private = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user.username}"

    class Meta:
        """Metaclass with table representation info."""

        ordering = ("-id",)
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def get_feed_posts(self):
        from ..posts.models import Post

        followers = Follower.objects.filter(follower=self)
        posts = list(Post.objects.filter(creator__in=[f.follow_to for f in followers]).order_by("-created_at")[:15])
        random.shuffle(posts)
        return posts

    def get_posts_groups(self):
        from ..posts.models import PostsGroup

        return PostsGroup.objects.filter(creator=self)


class Follower(BaseModel):
    """Follower model definition"""

    follower = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name="followers")
    follow_to = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name="followed")

    def __str__(self) -> str:
        return f"{self.follower} follow to {self.follow_to}"

    class Meta:
        verbose_name = "Follower"
        verbose_name_plural = "Followers"
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
        from ..chats.models import Elected
        from ..posts.models import PostsGroup

        with transaction.atomic():
            profile = Profile.objects.create(user=kwargs.get("instance"))
            Elected.objects.create(creator=profile)
            PostsGroup.objects.create(title="saved", creator=profile)
