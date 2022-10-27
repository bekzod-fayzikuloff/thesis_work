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


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    pass


@admin.register(Elected)
class ElectedAdmin(admin.ModelAdmin):
    pass


@admin.register(PrivateChat)
class PrivateChatAdmin(admin.ModelAdmin):
    form = PrivateChatForm
