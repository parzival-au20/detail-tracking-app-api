from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from core.models import Album, Photo


class AlbumPhotoViewSetTest(APITestCase):
    """Test the Album and Photo API endpoints."""

    def setUp(self):
        """Set up test users, albums, and photos."""
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='password123'
        )
        self.other_user = get_user_model().objects.create_user(
            email='otheruser@example.com',
            password='password123'
        )
        self.client.force_authenticate(user=self.user)

        # Create Albums
        self.album = Album.objects.create(user_pk=self.user, title="Test Album")
        self.other_album = Album.objects.create(user_pk=self.other_user, title="Other Album")

        # Create Photos
        self.photo = Photo.objects.create(
            album_pk=self.album,
            title="Test Photo",
            url="http://example.com/photo.jpg",
            thumbnailUrl="http://example.com/photo_thumb.jpg"
        )

        # API Endpoints
        self.album_url = '/api/users/{}/albums/'.format(self.user.id)  # URL for user's albums
        self.photo_url = '/api/users/{}/albums/{}/photos/'.format(self.user.id, self.album.id)  # URL for album's photos
        self.album_photos_url = '/api/users/{}/albums/{}/photos/'.format(self.user.id, self.album.id)  # Photos for album
        self.album_detail_url = '/api/users/{}/albums/{}/'.format(self.user.id, self.album.id)  # Specific album URL

    def test_get_user_albums(self):
        """Test retrieving albums for a specific user."""
        response = self.client.get(self.album_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one album for the user
        self.assertEqual(response.data[0]['title'], self.album.title)

    def test_get_album_photos(self):
        """Test retrieving photos for a specific album."""
        response = self.client.get(self.album_photos_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one photo in the album
        self.assertEqual(response.data[0]['title'], self.photo.title)

    def test_create_album(self):
        """Test creating a new album."""
        data = {"title": "New Album"}
        response = self.client.post(self.album_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Album.objects.filter(user_pk=self.user).count(), 2)

    def test_create_photo(self):
        """Test creating a new photo."""
        data = {
            "album_pk": self.album.id,
            "title": "New Photo",
            "url": "http://example.com/newphoto.jpg",
            "thumbnailUrl": "http://example.com/newphoto_thumb.jpg",
            "user_pk": self.user.id
        }
        response = self.client.post(self.photo_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Photo.objects.filter(album_pk=self.album).count(), 2)

    def test_delete_album(self):
        """Test deleting an album."""
        url = self.album_detail_url
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Album.objects.filter(id=self.album.id).exists())

    def test_delete_photo(self):
        """Test deleting a photo."""
        url = f'{self.photo_url}{self.photo.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Photo.objects.filter(id=self.photo.id).exists())

    def test_patch_album(self):
        """Test partially updating an album."""
        url = self.album_detail_url
        data = {"title": "Updated Album Title"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.album.refresh_from_db()
        self.assertEqual(self.album.title, "Updated Album Title")

    def test_patch_photo(self):
        """Test partially updating a photo."""
        url = f'{self.photo_url}{self.photo.id}/'
        data = {"title": "Updated Photo Title"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.photo.refresh_from_db()
        self.assertEqual(self.photo.title, "Updated Photo Title")

    def test_unauthorized_access(self):
        """Test that unauthenticated users cannot access endpoints."""
        self.client.logout()

        # Attempt to get user albums
        response = self.client.get(self.album_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Attempt to create an album
        response = self.client.post(self.album_url, {"title": "Unauthorized Album"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
