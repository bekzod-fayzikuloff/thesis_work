from rest_framework import routers

from . import views

chats_router = routers.SimpleRouter()
chats_router.register("", views.ChatViewSet, basename="chat")
message_router = routers.SimpleRouter()
message_router.register("", views.MessageViewSet, basename="message")

chats_urlpatterns = []
messages_urlpatterns = []

chats_urlpatterns += chats_router.urls
messages_urlpatterns += message_router.urls
