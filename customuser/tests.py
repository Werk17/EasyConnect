from typing_extensions import Required
from django.test import TestCase
from .models import CustomUser

class CustomUserTest(TestCase):
    def test_create_user(self):
        CustomUser.objects.create_user(
            username='testuser',
            phone_number='+123456789',
            password='testpassword',
            Organization_name='testorg',
        )

    def Test_account_Creation(self):
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.first().username, 'testuser')
        self.assertEqual(CustomUser.objects.first().phone_number, '+123456789')
        self.assertEqual(CustomUser.objects.first().Organization_name, 'testorg')
    
    def test_create_superuser(self):
        CustomUser.objects.create_superuser(
            username='testuser',
            phone_number='+123456789',
            password='testpassword',
            Organization_name='testorg',
        )
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.first().username, 'testuser')
        self.assertEqual(CustomUser.objects.first().phone_number, '+123456789')
        self.assertEqual(CustomUser.objects.first().Organization_name, 'testorg')
        self.assertTrue(CustomUser.objects.first().is_superuser)
        self.assertTrue(CustomUser.objects.first().is_staff)
