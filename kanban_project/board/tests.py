from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Task
from rest_framework import status
from django.test import TestCase


class CustomLoginViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login(self):
        url = reverse('login') 
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data) 
        token = response.data['token']
        self.assertTrue(Token.objects.filter(key=token).exists())
        
        
class CreateUserViewTest(APITestCase):
    def test_create_user_success(self):
        url = reverse('CreateUserView') 
        data = {
            'newUsername': 'testuser',
            'newPassword': 'testpassword',
            'newEmail': 'testuser@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('user_id', response.data)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)
        user_id = response.data['user_id']
        self.assertTrue(User.objects.filter(id=user_id).exists())


    def test_create_user_missing_fields(self):
        url = reverse('CreateUserView')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)
        self.assertIn('Username is required', response.data['error'])
        self.assertFalse(User.objects.filter(username='testuser').exists())
        
        
class TaskViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.client.force_authenticate(user=self.user)

    def test_get_tasks(self):
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if response.data:
            self.assertTrue('title' in response.data[0])


    def test_create_task(self):
        url = reverse('task-list')
        data = {'title': 'New Task', 'description': 'Description of New Task', 'created_by': self.user.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('title' in response.data)
        self.assertEqual(response.data['title'], 'New Task')
        
        
class TaskUpdateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.task = Task.objects.create(title='Test Task', description='Test Description', created_by=self.user)

    def test_delete_task(self):
        url = reverse('task-update-delete', kwargs={'pk': self.task.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_update_task(self):
        url = reverse('task-update-delete', kwargs={'pk': self.task.pk})
        data = {'title': 'Updated Task', 'description': 'Updated Description'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get(pk=self.task.pk).title, 'Updated Task')