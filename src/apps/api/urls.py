from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from common.utils.hooks import include_object

docs_urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]


urlpatterns = [
    path("auth/", include("apps.authentication.urls")),
    path("chats/", include(include_object("apps.chats.urls:chats_urlpatterns"))),
    path("messages/", include(include_object("apps.chats.urls:messages_urlpatterns"))),
    path("followers/", include(include_object("apps.profiles.urls:followers_urlpatterns"))),
    path("profiles/", include("apps.profiles.urls")),
    path("privatechats/", include(include_object("apps.chats.urls:private_chats_urlpatterns"))),
    path("posts/", include(include_object("apps.posts.urls:posts_urlpatterns"))),
    path("reactions/", include(include_object("apps.posts.urls:reactions_urlpatterns"))),
    path("posts-groups/", include(include_object("apps.posts.urls:posts_groups_urlpatterns"))),
    path("comments/", include(include_object("apps.posts.urls:comments_urlpatterns"))),
    path("docs/", include(docs_urlpatterns)),
]
