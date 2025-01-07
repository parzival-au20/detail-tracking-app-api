"""
Serializers for the posts API View
"""

from core.models import Post, Comment
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    """ Serializer for the post object."""
    # user_id = serializers.CharField(source='user.id', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user_id', 'title', 'body']


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for the comment object."""
    name = serializers.CharField(source='user.name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Comment
        fields = ['post', 'id', 'name', 'email', 'body']
