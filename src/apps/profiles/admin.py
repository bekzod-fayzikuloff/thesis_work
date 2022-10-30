from django.contrib import admin

from .models import Follower, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)
    list_filter = ("user__is_active",)
    search_fields = ("user__username", "user__email")


@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    list_display_links = ("__str__",)
    search_fields = (
        "follower__user__username",
        "follower__user__email",
        "follow_to__user__username",
        "follow_to__user__email",
    )
