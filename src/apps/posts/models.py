import functools

from django.core.validators import FileExtensionValidator
from django.db import models

from apps.profiles.models import Profile
from common.models import BaseModel
from common.validators import validate_file_size


class PostMedia(BaseModel):
    """PostMedia model definition."""

    file = models.FileField(
        upload_to="posts/media/%Y/%m/%d/",
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "png", "gif", "bmp", "ico", "mp4", "webm", "avi"]),
            functools.partial(validate_file_size, max_size=10485760),
        ],
    )

    def __str__(self) -> str:
        return f"Posts {self.id} media"

    class Meta:
        verbose_name = "Post media"
        verbose_name_plural = "Posts medias"


class PostsGroup(models.Model):
    """PostsGroup model definition"""

    title = models.CharField(max_length=255)
    creator = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="posts_groups", related_query_name="posts_group"
    )
    posts = models.ManyToManyField(to="Post", blank=True, related_name="groups")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.title})"

    class Meta:
        verbose_name = "Posts group"
        verbose_name_plural = "Posts groups"


class Post(BaseModel):
    """Post model definition."""

    description = models.TextField(max_length=1000)
    creator = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name="posts", related_query_name="posts")
    medias = models.ManyToManyField(to=PostMedia, related_name="posts", related_query_name="posts")
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"User {self.creator.user.username} post {self.description[:10]}..."

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"


class Comment(BaseModel):
    """Comment model definition."""

    content = models.TextField(max_length=500, db_index=True)
    creator = models.ForeignKey(to=Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Comment by {self.creator.user.username} to {self.post}"

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"


class Reaction(BaseModel):
    """Reaction model definition."""

    creator = models.ForeignKey(to=Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)

    is_positive = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"Reaction by {self.creator.user.username} to {self.post}"

    class Meta:
        verbose_name = "Reaction"
        verbose_name_plural = "Reactions"
