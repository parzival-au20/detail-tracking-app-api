"""
Tests for the todo API.
"""
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from core.models import ToDo
from rest_framework.test import APIClient


class ToDoViewSetTest(APITestCase):
    """Test the ToDo API endpoints"""

    def setUp(self):
        """Create user and a sample ToDo for testing."""
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='password123'
        )
        self.client.force_authenticate(user=self.user)

        # Create a sample ToDo
        self.todo = ToDo.objects.create(
            user_pk=self.user,
            title="Test ToDo",
            completed=False,
        )

        # URL pattern with user_pk
        self.todo_url = f'/api/users/{self.user.id}/todos/'

    def test_get_todos_for_authenticated_user(self):
        """Test retrieving to-do list for authenticated user"""
        response = self.client.get(self.todo_url)
        todos = ToDo.objects.filter(user_pk=self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), todos.count())

    def test_create_todo_for_authenticated_user(self):
        """Test creating a new to-do item."""
        data = {
            "title": "New ToDo",
            "completed": False,
            'user_pk': self.user.id
        }
        response = self.client.post(self.todo_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ToDo.objects.count(), 2)
        self.assertEqual(ToDo.objects.latest('id').title, "New ToDo")

    def test_get_user_todos(self):
        """Test retrieving all to-dos for a specific user."""
        url = f'/api/users/{self.user.id}/todos/'
        response = self.client.get(url)
        todos = ToDo.objects.filter(user_pk=self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), todos.count())

    def test_get_single_todo(self):
        """Test retrieving a single to-do for a user."""
        url = f'/api/users/{self.user.id}/todos/{self.todo.id}/'  # URL güncellendi
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.todo.id)

    def test_user_todos_not_found(self):
        """Test that a 404 is returned if the user does not exist."""
        invalid_user_id = 9999
        url = f'/api/users/{invalid_user_id}/todos/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], "A user with the specified user_id was not found.")

    def test_unauthenticated_user_access(self):
        """Test that unauthenticated users cannot access to-do items."""
        self.client.logout()  # Logout to make the client unauthenticated
        response = self.client.get(self.todo_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_todo(self):
        """Test deleting a specific to-do."""
        url = f'{self.todo_url}{self.todo.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ToDo.objects.filter(id=self.todo.id).count(), 0)

    def test_update_todo_with_patch(self):
        """Test partially updating a to-do (PATCH)."""
        url = f'{self.todo_url}{self.todo.id}/'
        data = {"title": "Updated Title"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, "Updated Title")

    def test_update_todo_with_put(self):
        """Test updating a to-do completely (PUT)."""
        url = f'{self.todo_url}{self.todo.id}/'
        data = {
            "title": "Completely Updated Title",
            "completed": True,
            'user_pk': self.user.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, "Completely Updated Title")
        self.assertEqual(self.todo.completed, True)

    def test_delete_todo_unauthorized(self):
        """Test that an unauthenticated user cannot delete a to-do."""
        self.client.logout()
        url = f'{self.todo_url}{self.todo.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(ToDo.objects.filter(id=self.todo.id).exists())  # To-Do hâlâ duruyor mu?

    def test_patch_todo_unauthorized(self):
        """Test that an unauthenticated user cannot patch a to-do."""
        self.client.logout()
        url = f'{self.todo_url}{self.todo.id}/'
        data = {"title": "Unauthorized Update"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.todo.refresh_from_db()
        self.assertNotEqual(self.todo.title, "Unauthorized Update")

    def test_put_todo_unauthorized(self):
        """Test that an unauthenticated user cannot update a to-do."""
        self.client.logout()
        url = f'{self.todo_url}{self.todo.id}/'
        data = {
            "title": "Unauthorized Full Update",
            "completed": True,
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.todo.refresh_from_db()
        self.assertNotEqual(self.todo.title, "Unauthorized Full Update")
        self.assertNotEqual(self.todo.completed, True)
