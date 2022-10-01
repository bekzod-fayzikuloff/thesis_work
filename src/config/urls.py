from django.contrib import admin
from django.urls import include, path, re_path

from common.utils.docs_schema import schema_view

docs_urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

api_patterns = [
    path("", include("apps.api.urls")),
]

urlpatterns = [
    path("api/", include(api_patterns)),
    path("docs/", include(docs_urlpatterns)),
    path("admin/", admin.site.urls),
]
