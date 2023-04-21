from django_filters import rest_framework as filters

from .models import Comment, Post


class PostFilter(filters.FilterSet):
    created_by = filters.NumberFilter(field_name="creator__id", lookup_expr="exact")

    class Meta:
        model = Post
        fields = ("description",)


class CommentFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name="creator__user__username", lookup_expr="icontains")
    post_id = filters.NumberFilter(field_name="post__pk", lookup_expr="exact")

    class Meta:
        model = Comment
        fields = ("created_by", "content", "post_id")
