from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = []

router = DefaultRouter()
router.register(r"", views.ProfileViewSet, basename="profile")
urlpatterns += router.urls
