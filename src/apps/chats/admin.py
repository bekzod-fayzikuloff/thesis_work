from django.contrib import admin

from .models import Chat, Elected, Media, Message


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    pass


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    pass


@admin.register(Elected)
class ElectedAdmin(admin.ModelAdmin):
    pass
