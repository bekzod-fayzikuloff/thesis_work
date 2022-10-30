from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

docs_urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

urlpatterns = [
    path("auth/", include("apps.authentication.urls")),
    path("chats/", include("apps.chats.urls")),
    path("profiles/", include("apps.profiles.urls")),
    path("docs/", include(docs_urlpatterns)),
]
