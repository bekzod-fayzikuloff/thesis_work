from django_filters import rest_framework as filters

from .models import Follower, Profile


class ProfileFilter(filters.FilterSet):
    username = filters.CharFilter(field_name="user__username", lookup_expr="icontains")

    class Meta:
        model = Profile
        fields = ("username", "description")


class FollowerFilter(filters.FilterSet):
    username = filters.CharFilter(field_name="follower__user__username", lookup_expr="icontains")

    class Meta:
        model = Follower
        fields = ("username",)
