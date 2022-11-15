from rest_framework import routers

from . import views

chats_router = routers.SimpleRouter()
chats_router.register("", views.ChatViewSet, basename="chat")

message_router = routers.SimpleRouter()
message_router.register("", views.MessageViewSet, basename="message")

private_chats_router = routers.SimpleRouter()
private_chats_router.register("", views.PrivateChatViewSet, basename="private_chat")

chats_urlpatterns = []
messages_urlpatterns = []
private_chats_urlpatterns = []

chats_urlpatterns += chats_router.urls
messages_urlpatterns += message_router.urls
private_chats_urlpatterns += private_chats_router.urls
