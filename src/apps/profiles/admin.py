from django.contrib import admin

from .models import Comment, Follower, Post, PostMedia, PostsGroup, Profile, Reaction


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


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ("creator__user__username", "creator__user__email", "description")
    list_filter = ("is_active",)
    filter_horizontal = ("medias",)


@admin.register(PostMedia)
class PostMediaAdmin(admin.ModelAdmin):
    list_display_links = ("__str__",)


@admin.register(PostsGroup)
class PostsGroupAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title", "creator__user__username")
    filter_horizontal = ("posts",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = ("content", "creator__user__email", "creator__user__username", "post__description")


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    search_fields = ("creator__user__email", "creator__user__username", "post__description")
    list_filter = ("is_positive", "is_active")
