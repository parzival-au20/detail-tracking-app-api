"""
Views for the Albums API.
"""
from rest_framework import viewsets, authentication, permissions
from core.models import Album, Photo, User
from album.serializers import AlbumSerializer, PhotoSerializer
from django_filters.rest_framework import DjangoFilterBackend

class AlbumViewSet(viewsets.ModelViewSet):
    """Manage Album in the database."""
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']

    def perform_create(self, serializer):
        """create a new album."""
        user_pk = self.kwargs.get('user')
        user = User.objects.get(id=user_pk)
        serializer.save(user=user)


class PhotoViewSet(viewsets.ModelViewSet):
    """Manage photos in the database."""
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['album']

    def perform_create(self, serializer):
        """Yeni fotoğraf oluştur."""
        album_pk = self.request.data.get('album')
        album = Album.objects.get(id=album_pk)
        user = album.user
        serializer.save(album=album, user=user)
