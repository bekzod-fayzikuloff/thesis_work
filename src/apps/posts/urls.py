from rest_framework.routers import SimpleRouter

from . import views

post_router = SimpleRouter()
post_router.register("", views.PostViewSet, basename="post")

comment_router = SimpleRouter()
comment_router.register("", views.CommentViewSet, basename="comment")
posts_urlpatterns = []
comments_urlpatterns = []

posts_urlpatterns += post_router.urls
comments_urlpatterns += comment_router.urls
