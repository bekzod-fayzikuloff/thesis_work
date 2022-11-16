from django_filters import rest_framework as filters

from .models import Chat, Message, PrivateChat


class ChatFilter(filters.FilterSet):
    class Meta:
        model = Chat
        fields = ("title", "description")


class PrivateChatFilter(filters.FilterSet):
    class Meta:
        model = PrivateChat
        fields = ("first_member__user__username", "second_member__user__username")


class MessageFilter(filters.FilterSet):
    creator = filters.CharFilter(field_name="maker__user__username", lookup_expr="icontains")

    class Meta:
        model = Message
        fields = ("creator", "content")
