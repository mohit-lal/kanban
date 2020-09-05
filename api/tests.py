from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import *
from rest_framework.test import APIClient

# class TestUserLogin(TestCase):
#     def setUp(self):
#         self.user = User.objects.create(username='testUser')
#         self.user.set_password('test123')
#         self.user.save()
#         self.url = reverse('api:login')


#     def test_invalid_credentials(self):
#         response = self.client.post(self.url, data={'username': 'test', 'password':'password123'})
#         self.assertEqual(response.status_code, 400)

#     def test_valid_credentials(self):
#         response = self.client.post(self.url, data={'username': 'testUser', 'password': 'test123'})
#         self.assertEqual(response.status_code, 200)







