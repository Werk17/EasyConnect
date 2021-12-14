from django.test import TestCase
from .models import Announcement

class AnnouncementTest(TestCase):
    def test_str(self):
        test_announcement = Announcement(id=1, body="My first announcement")
        self.assertEqual(str(test_announcement.body), 'My first announcement')
    
    def test_ordering(self):

        first_announcement = Announcement.objects.create(id= 1)
        second_announcement = Announcement.objects.create(id= 2)
        third_announcement = Announcement.objects.create(id= 3)

        self.assertEqual(
            list(Announcement.objects.all()),
            [first_announcement, second_announcement, third_announcement]
        )
    
    def test_announcement_content(self):
        test_announcement = Announcement.objects.create(
            id=1,
            body='This is the content of my first announcement'
        )
        self.assertEqual(test_announcement.body, 'This is the content of my first announcement')
