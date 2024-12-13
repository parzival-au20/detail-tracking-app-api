"""
Tests for the post API.
"""
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from core.models import Post, Comment
from django.urls import reverse
from rest_framework.test import APIClient


class PostTests(APITestCase):

    def setUp(self):
        """Test için gerekli verileri oluşturuyoruz."""
        # Kullanıcı oluşturma
        self.client = APIClient()
        User = get_user_model()
        self.user = User.objects.create_user(email="user@example.com", password='testpassword')

        # Get token for authentication
        token_url = reverse('user:token')
        response = self.client.post(token_url, {
            'email': 'user@example.com',
            'password': 'testpassword'
        })

        self.token = response.data.get('token')  # Token'dan `token` alın
        self.assertIsNotNone(self.token, "Token alınamadı!")

        # Add token to authorization header
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Post oluşturma
        self.post = Post.objects.create(
            title="Test Post",
            body="This is a test post",
            user_pk=self.user
        )

        # Yorum oluşturma
        self.comment = Comment.objects.create(
            post_pk=self.post,
            body="This is a test comment",
            user_pk=self.user
        )

    def test_create_post(self):
        """Yeni bir post oluşturma."""
        url = f'/api/users/{self.user.id}/posts/'
        data = {'title': 'New Post', 'body': 'Post body', 'user_pk': self.user.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)  # Bir post daha olmalı

    def test_get_posts(self):
        """Postları listeleme."""
        url = f'/api/users/{self.user.id}/posts/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # İlk başta sadece bir post olmalı

    def test_get_post_detail(self):
        """Post detayını alma."""
        url = f'/api/users/{self.user.id}/posts/{self.post.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.post.title)

    def test_create_comment(self):
        """Bir post için yorum ekleme."""
        url = f'/api/users/{self.user.id}/posts/{self.post.id}/comments/'
        data = {'body': 'This is a test comment', 'post_pk': self.post.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)  # Bir yorum daha olmalı

    def test_get_comments(self):
        """Bir postun yorumlarını listeleme."""
        url = f'/api/users/{self.user.id}/posts/{self.post.id}/comments/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Yalnızca bir yorum olmalı

    def test_get_comment_detail(self):
        """Yorum detayını alma."""
        url = f'/api/users/{self.user.id}/posts/{self.post.id}/comments/{self.comment.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['body'], self.comment.body)

    def test_update_post(self):
        """Test that a user can update post."""
        url = f'/api/users/{self.user.id}/posts/{self.post.id}/'
        data = {'title': 'Updated Title', 'body': 'Updated Body'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, data['title'])
        self.assertEqual(self.post.body, data['body'])

    def test_update_comment(self):
        """Test that a user can update their own comment."""
        url = f'/api/users/{self.user.id}/posts/{self.post.id}/comments/{self.comment.id}/'
        data = {'body': 'Updated comment body'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.comment.refresh_from_db()
        self.assertEqual(self.comment.body, data['body'])

    def test_delete_post(self):
        """Test deleting a user's post."""
        url = f'/api/users/{self.user.id}/posts/{self.post.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_delete_comment(self):
        """Test that a user can delete their own comment."""
        url = f'/api/users/{self.user.id}/posts/{self.post.id}/comments/{self.comment.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())

    def test_create_post_without_auth(self):
        """Test creating post without authentication."""
        self.client.credentials()  # Token'ı kaldırıyoruz.
        url = f'/api/users/{self.user.id}/posts/'
        data = {'title': 'Unauthenticated Post', 'body': 'No auth body'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_comment_without_auth(self):
        """Test creating comment without authentication."""
        self.client.credentials()  # Token'ı kaldırıyoruz.
        url = f'/api/users/{self.user.id}/posts/{self.post.id}/comments/'
        data = {'body': 'No auth comment'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_posts_without_auth(self):
        """Test getting posts without authentication."""
        self.client.credentials()  # Token'ı kaldırıyoruz.
        url = f'/api/users/{self.user.id}/posts/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_comments_without_auth(self):
        """Test getting comments without authentication."""
        self.client.credentials()  # Token'ı kaldırıyoruz.
        url = f'/api/users/{self.user.id}/posts/{self.post.id}/comments/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_post_without_auth(self):
        """Test deleting post without authentication."""
        self.client.credentials()  # Token'ı kaldırıyoruz.
        url = f'/api/users/{self.user.id}/posts/{self.post.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_comment_without_auth(self):
        """Test deleting comment without authentication."""
        self.client.credentials()  # Token'ı kaldırıyoruz.
        url = f'/api/users/{self.user.id}/posts/{self.post.id}/comments/{self.comment.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
