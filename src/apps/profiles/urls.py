from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [path("me/", views.index)]

router = DefaultRouter()
router.register(r"users", views.ProfileViewSet, basename="user")
urlpatterns += router.urls
