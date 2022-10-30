from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .forms import PrivateChatForm
from .models import Chat, Elected, Media, Message, PrivateChat


class MessageInline(GenericTabularInline):
    model = Message
    ct_field = "chat_type"
    ct_fk_field = "chat_id"
    fk_name = "chat_object"


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    inlines = [MessageInline]
    list_display = ("title", "flatten_members")
    search_fields = ("title", "description", "members__user__username")
    filter_horizontal = ("members",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    search_fields = ("title", "description", "members__user__username", "members__user__email")
    filter_horizontal = ("medias",)


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    search_fields = ("messages__content", "messages__maker__user__username")


@admin.register(Elected)
class ElectedAdmin(admin.ModelAdmin):
    filter_horizontal = ("messages",)
    search_fields = ("messages__content", "creator__user__username")


@admin.register(PrivateChat)
class PrivateChatAdmin(admin.ModelAdmin):
    search_fields = (
        "first_member__user__username",
        "first_member__user__email",
        "second_member__user__username",
        "second_member__user__email",
    )

    inlines = [MessageInline]
    form = PrivateChatForm
