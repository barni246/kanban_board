from django.test import TestCase
from .models import Task
from django.contrib.auth.models import User

class MyModelTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser')
        Task.objects.create(title="Test", description="Test description", created_by=user)

    def test_my_model(self):
        obj = Task.objects.get(title="Test")
        self.assertEqual(obj.title, "Test")
