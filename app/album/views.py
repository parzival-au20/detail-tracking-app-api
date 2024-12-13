"""
Views for the Albums API.
"""
from rest_framework import viewsets, authentication, permissions
from core.models import Album, Photo, User
from album.serializers import AlbumSerializer, PhotoSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    """Manage Album in the database."""
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_pk = self.kwargs.get('user_pk')
        if user_pk:
            return self.queryset.filter(user_pk=user_pk)
        return self.queryset

    def perform_create(self, serializer):
        """create a new album."""
        user_pk = self.kwargs.get('user_pk')
        user = User.objects.get(id=user_pk)
        serializer.save(user_pk=user)


class PhotoViewSet(viewsets.ModelViewSet):
    """Manage photos in the database."""

    serializer_class = PhotoSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Albüm bazlı fotoğrafları getir."""
        album_pk = self.kwargs.get('album_pk')
        if album_pk:
            return Photo.objects.filter(album_pk=album_pk)
        return Photo.objects.all()

    def perform_create(self, serializer):
        """Yeni fotoğraf oluştur."""
        album_pk = self.kwargs.get('album_pk')
        album = Album.objects.get(id=album_pk)
        serializer.save(album_pk=album, user_pk=self.request.user)
