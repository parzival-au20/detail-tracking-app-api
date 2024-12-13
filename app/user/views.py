"""
Views for the user API.
"""
from rest_framework import viewsets, authentication, permissions
from core.models import User
from user.serializers import UserSerializer, AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.decorators import action
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    """Manage users in the system."""
    serializer_class = UserSerializer
    queryset = User.objects.all()  # Tüm kullanıcıları sorgula
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Override perform_create to handle user creation"""
        serializer.save()

    def get_permissions(self):
        """
        Override get_permissions to handle authentication only on non-create operations.
        """
        if self.action == 'create':
            # POST işlemi (create) için kimlik doğrulama gerekmiyor
            return []  # Kimlik doğrulaması gerekmiyor
        return [permission() for permission in self.permission_classes]

    @action(detail=False, methods=['get'], url_path='city')
    def filter_by_city(self, request):
        """
        Filter users by city information.
        /api/users/city/?city="city"
        """
        city = request.query_params.get('city')
        if not city:
            return Response({"detail": "City parameter is required."}, status=400)

        users = self.queryset.filter(address__city__iexact=city)
        if not users.exists():
            return Response({"detail": "No users found for the given city."}, status=404)

        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
