import functools
import uuid

from django.db import models

from apps.profiles.models import Profile
from common.models import BaseModel
from common.validators import validate_file_size


class Chat(BaseModel):
    """Описание таблицы Чатов"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField("Название", max_length=255, db_index=True)
    description = models.TextField("Описание", max_length=500, null=True)
    members = models.ManyToManyField(to=Profile, blank=True, related_name="chats", verbose_name="Участники")

    class Meta:
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"

    def __str__(self) -> str:
        return f"Chat ({self.title})"


class Media(BaseModel):
    file = models.FileField(
        upload_to="messages/media/%Y/%m/%d/",
        validators=[
            functools.partial(validate_file_size, max_size=10485760 * 100),
        ],
    )

    def __str__(self) -> str:
        return f"Message({self.id}) media"

    class Meta:
        verbose_name = "Meдия сообщения"
        verbose_name_plural = "Медия сообщений"


class Message(BaseModel):
    """Описание таблицы сообщение"""

    content = models.TextField("Содержимое", max_length=1000, blank=True)
    maker = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="messages", related_query_name="message")
    to_chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages", related_query_name="message")
    answer = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="replies", related_query_name="reply"
    )
    medias = models.ManyToManyField(to=Media, symmetrical=False)
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Message({self.id}) to chat({self.to_chat.title})"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Elected(BaseModel):
    """Описание таблицы сообщение `Избранное`"""

    creator = models.OneToOneField(to=Profile, on_delete=models.CASCADE, related_name="elected_messages")
    messages = models.ManyToManyField(to=Message, blank=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.creator.user.username})"

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"
