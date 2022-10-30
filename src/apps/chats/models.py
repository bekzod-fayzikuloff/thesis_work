import functools
import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from apps.chats.exceptions import PrivateChatAlreadyExistsError
from apps.profiles.models import Profile
from common.models import BaseModel
from common.validators import validate_file_size


class Chat(BaseModel):
    """Описание таблицы Чатов"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField("Название", max_length=255, db_index=True)
    description = models.TextField("Описание", max_length=500, blank=True)
    members = models.ManyToManyField(to=Profile, blank=True, related_name="chats", verbose_name="Участники")

    @property
    def flatten_members(self):
        return ", ".join(member.user.username for member in self.members.filter()[:10])

    class Meta:
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"

    def __str__(self) -> str:
        return f"Chat ({self.title})"


class PrivateChat(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_member = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, verbose_name="Первый участник", related_name="+"
    )
    second_member = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, verbose_name="Второй участник", related_name="+"
    )

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """Описание логики сохранения чата с личной группой в которой происходит проверка на уникальность группы"""
        qs = PrivateChat.objects.filter(first_member=self.second_member, second_member=self.first_member)
        for privatechat in qs:
            if privatechat.id != self.id:
                raise PrivateChatAlreadyExistsError("Chat with same users already exists")
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def __str__(self) -> str:
        return f"Private chat with [{self.first_member}, {self.second_member}]"

    class Meta:
        verbose_name = "Личное"
        verbose_name_plural = "Личные"
        unique_together = (("first_member", "second_member"),)
        constraints = [
            models.CheckConstraint(
                check=(~models.Q(first_member=models.F("second_member"))),
                name="check_private_member",
                violation_error_message="Users cannot send message to themselves.",
            )
        ]


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

    limit = models.Q(app_label="chats", model="chat") | models.Q(app_label="chats", model="privatechat")

    content = models.TextField("Содержимое", max_length=1000, blank=True)
    maker = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="messages", related_query_name="message")
    chat_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=limit)
    chat_id = models.UUIDField()
    chat_object = GenericForeignKey("chat_type", "chat_id")
    answer = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="replies", related_query_name="reply"
    )
    medias = models.ManyToManyField(to=Media, related_name="messages", related_query_name="messages", blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Message({self.id}) to chat({self.chat_type.get_object_for_this_type(id=self.chat_id)})"

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
