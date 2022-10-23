from django.contrib import admin

from .models import Follower, Post, PostMedia, PostsGroup, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(PostMedia)
class PostMediaAdmin(admin.ModelAdmin):
    pass


@admin.register(PostsGroup)
class PostsGroupAdmin(admin.ModelAdmin):
    pass
