from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class UserProfileTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_profile_creation(self):
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertEqual(self.user.profile.user, self.user)

    def test_profile_update(self):
        profile = self.user.profile
        profile.bio = 'Test bio'
        profile.department = 'Development'
        profile.skills = 'Python,Django'
        profile.save()
        self.assertEqual(profile.bio, 'Test bio')
        self.assertEqual(profile.department, 'Development')
        self.assertEqual(profile.skills, 'Python,Django')

    def test_csrf_protection(self):
        response = self.client.post('/users/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 403)  # Should fail without CSRF token

        # Test with CSRF token
        response = self.client.get('/users/login/')
        csrf_token = response.cookies['csrftoken'].value
        response = self.client.post('/users/login/', {
            'username': 'testuser',
            'password': 'testpass123',
            'csrfmiddlewaretoken': csrf_token
        }, HTTP_X_CSRFTOKEN=csrf_token)
        self.assertEqual(response.status_code, 302)  # Should redirect on success