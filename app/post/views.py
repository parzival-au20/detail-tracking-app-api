"""
Views for the Posts API.
"""
from rest_framework import viewsets, authentication, permissions
from django_filters.rest_framework import DjangoFilterBackend
from core.models import Post, Comment, User
from post.serializers import PostSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    """Manage posts in the database."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]  # Sadece giriş yapan kullanıcılar görebilir.

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']


    def perform_create(self, serializer):
        """Create a new post."""
        user_pk = self.kwargs.get('user_pk')
        user = User.objects.get(id=user_pk)
        serializer.save(user_pk=user)


class CommentViewSet(viewsets.ModelViewSet):
    """Manage comments in the database."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]  # Sadece giriş yapan kullanıcılar görebilir.

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post']

    def perform_create(self, serializer):
        """create a new comment."""
        post_pk = self.kwargs.get('post')
        post = Post.objects.get(id=post_pk)
        serializer.save(post_pk=post, user_pk=self.request.user)
