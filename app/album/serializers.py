"""
Serializers for the album API View
"""

from core.models import Album, Photo

from rest_framework import serializers


class AlbumSerializer(serializers.ModelSerializer):
    """ Serializer for the album object."""
    # photos = serializers.StringRelatedField(many=True, read_only=True)
    # user = serializers.CharField(source='user.id', read_only=True)

    class Meta:
        model = Album
        fields = ['user', 'id', 'title']


class PhotoSerializer(serializers.ModelSerializer):
    """Serializer for the photo object."""

    class Meta:
        model = Photo
        fields = ['album', 'id', 'title', 'url', 'thumbnailUrl']
