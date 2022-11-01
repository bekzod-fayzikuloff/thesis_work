from rest_framework.routers import SimpleRouter

from . import views

urlpatterns = []
followers_urlpatterns = []

profile_router = SimpleRouter()
profile_router.register(r"", views.ProfileViewSet, basename="profile")

followers_router = SimpleRouter()
followers_router.register(r"", views.FollowerViewSet, basename="follower")

followers_urlpatterns += followers_router.urls
urlpatterns += profile_router.urls
