"""
Views for the To-Do API.
"""
from rest_framework import viewsets, authentication, permissions
from core.models import ToDo, User
from todo.serializers import ToDoSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django_filters.rest_framework import DjangoFilterBackend


class ToDoViewSet(viewsets.ModelViewSet):
    """Manage to-do in the database."""
    queryset = ToDo.objects.all()
    serializer_class = ToDoSerializer
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]  # Sadece giriş yapan kullanıcılar görebilir.

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']

    def perform_create(self, serializer):
        """Create a new todo."""
        user_pk = self.kwargs.get('user_pk')
        user = User.objects.get(id=user_pk)
        serializer.save(user_pk=user)

    @action(detail=False, methods=['get'], url_path='incomplete-todos')
    def get_incomplete_todos(self, request, user_pk=None):
        """Get all incomplete todos for a specific user."""
        user_pk = self.kwargs.get('user_pk')
        todos = ToDo.objects.filter(user_pk=user_pk, completed=False)
        serializer = self.get_serializer(todos, many=True)
        return Response(serializer.data)
