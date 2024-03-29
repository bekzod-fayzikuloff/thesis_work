from rest_framework.routers import SimpleRouter

from . import views

post_router = SimpleRouter()
post_router.register("", views.PostViewSet, basename="post")

posts_groups_router = SimpleRouter()
posts_groups_router.register("", views.PostGroupViewSet, basename="comment")

comment_router = SimpleRouter()
comment_router.register("", views.CommentViewSet, basename="comment")

reactions_router = SimpleRouter()
reactions_router.register("", views.ReactionViewSet, basename="reaction")

posts_urlpatterns = []
comments_urlpatterns = []
posts_groups_urlpatterns = []
reactions_urlpatterns = []

posts_urlpatterns += post_router.urls
posts_groups_urlpatterns += posts_groups_router.urls
comments_urlpatterns += comment_router.urls
reactions_urlpatterns += reactions_router.urls
