from django.contrib import admin
from django.urls import include, path

api_patterns = [
    path("", include("apps.api.urls")),
]

urlpatterns = [
    path("api/", include(api_patterns)),
    path("admin/", admin.site.urls),
]
