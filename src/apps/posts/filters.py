from django_filters import rest_framework as filters

from .models import Comment, Post


class PostFilter(filters.FilterSet):
    created_by = filters.NumberFilter(field_name="creator__id", lookup_expr="exact")

    class Meta:
        model = Post
        fields = ("description",)


class CommentFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name="creator__user__username", lookup_expr="icontains")

    class Meta:
        model = Comment
        fields = ("created_by", "content")
