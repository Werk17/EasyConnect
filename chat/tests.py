from datetime import time
from django.test import TestCase
from .models import Message
from customuser.models import CustomUser

class MessageTestCase(TestCase):
    def setUp(self):
        firstauthor = CustomUser.objects.create(username='test_user')
        secondauthor = CustomUser.objects.create(username='test_user2')
        Message.objects.create(content='First message', author=firstauthor, timestamp=time(hour=12, minute=0))
        Message.objects.create(content='Second message', author=secondauthor, timestamp=time(hour=12, minute=30))
    
    def test_message_count(self):
        self.assertEqual(Message.objects.count(), 2)

    def test_message_content(self):
        first_message = Message.objects.get(id=1)
        second_message = Message.objects.get(id=2)
        self.assertEqual(first_message.content, 'First message')
        self.assertEqual(second_message.content, 'Second message')

    def test_message_content_empty(self):
        message = Message.objects.get(id=1)
        message.content = ''
        message.save()
        self.assertEqual(message.content, '')

    def test_message_content_max_length(self):
        message = Message.objects.get(id=1)
        message.content = 'a' * 1000
        message.save()
        self.assertEqual(message.content, 'a' * 1000)

    def test_message_content_min_length(self):
        message = Message.objects.get(id=1)
        message.content = ''
        message.save()
        self.assertEqual(message.content, '')

    def test_message_content_default(self):
        message = Message.objects.get(id=1)
        self.assertEqual(message.content, 'First message')
