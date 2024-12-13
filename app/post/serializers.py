"""
Serializers for the posts API View
"""

from core.models import Post, Comment
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    """ Serializer for the post object."""
    user_pk = serializers.CharField(source='user.id', read_only=True)

    class Meta:
        model = Post
        fields = ['user_pk', 'id', 'title', 'body']


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for the comment object."""
    name = serializers.CharField(source='user_pk.name', read_only=True)
    email = serializers.EmailField(source='user_pk.email', read_only=True)

    class Meta:
        model = Comment
        fields = ['post_pk', 'id', 'name', 'email', 'body']
