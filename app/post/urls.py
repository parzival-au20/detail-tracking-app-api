"""
URL mappings for post API
"""


from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter
from post.views import PostViewSet, CommentViewSet

app_name = 'post'


# Main router
router = SimpleRouter()
router.register(r'users', PostViewSet, basename='users')

# Nested router for posts
posts_router = NestedSimpleRouter(router, r'users', lookup='user')
posts_router.register(r'posts', PostViewSet, basename='user-posts')

# Nested router for comments
comments_router = NestedSimpleRouter(posts_router, r'posts', lookup='post')
comments_router.register(r'comments', CommentViewSet, basename='post-comments')

urlpatterns = router.urls + posts_router.urls + comments_router.urls
