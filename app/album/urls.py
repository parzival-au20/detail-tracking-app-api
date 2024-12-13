"""
URL mappings for Album API
"""


from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter
from album.views import AlbumViewSet, PhotoViewSet

app_name = 'album'


# Main router
router = SimpleRouter()
router.register(r'users', AlbumViewSet, basename='users')

# Nested router for albums
albums_router = NestedSimpleRouter(router, r'users', lookup='user')
albums_router.register(r'albums', AlbumViewSet, basename='user-albums')

# Nested router for photos
photos_router = NestedSimpleRouter(albums_router, r'albums', lookup='album')
photos_router.register(r'photos', PhotoViewSet, basename='album-photos')

urlpatterns = router.urls + albums_router.urls + photos_router.urls
