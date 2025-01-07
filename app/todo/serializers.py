"""
Serializers for the to-do API View
"""

from core.models import ToDo

from rest_framework import serializers


class ToDoSerializer(serializers.ModelSerializer):
    """ Serializer for the to-do object."""

    user = serializers.CharField(source='user.id', read_only=True)

    class Meta:
        model = ToDo
        fields = ['user', 'id', 'title', 'completed']
