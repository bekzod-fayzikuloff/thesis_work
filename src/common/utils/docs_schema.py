from functools import lru_cache

from django.conf import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


@lru_cache
def get_schema_view_():
    docs_access_mode = (
        permissions.AllowAny if settings.DEBUG else permissions.IsAdminUser
    )
    return get_schema_view(
        openapi.Info(
            title=settings.DOCS_SCHEMA_TITLE,
            default_version=settings.DOCS_SCHEMA_VERSION,
            description=settings.DOCS_SCHEMA_DESCRIPTION,
            terms_of_service=settings.DOCS_SCHEMA_TERMS_OF_SERVICE,
            contact=openapi.Contact(email=settings.DOCS_SCHEMA_CONTACT_EMAIL),
            license=openapi.License(name=settings.DOCS_SCHEMA_LICENSE),
        ),
        public=settings.DOCS_SCHEMA_PUBLIC,
        permission_classes=[docs_access_mode],
    )


schema_view = get_schema_view_()
