from django.test import TestCase
from .models import Contact

class ContactUsTestCase(TestCase):
    def setup_contact_us(self):
        return Contact.objects.create(
            email='TestUser@gmail.com',
            subject='Test Subject',
            message='Test Message'
        )

    def test_contact_us_creation(self):
        contact_us = self.setup_contact_us()
        self.assertTrue(isinstance(contact_us, Contact))
        self.assertEqual(contact_us.__str__(), contact_us.email)

    def test_contact_us_creation_with_no_email(self):
        contact_us = Contact.objects.create(
            email='',
            subject='Test Subject',
            message='Test Message'
        )
        self.assertTrue(isinstance(contact_us, Contact))

    def test_contact_us_creation_with_no_subject(self):
        contact_us = Contact.objects.create(
            email='testuser@gmail.com',
            subject='',
            message='Test Message'
        )
        self.assertTrue(isinstance(contact_us, Contact))

    def test_contact_us_creation_with_no_message(self):
        contact_us = Contact.objects.create(
            email = 'testUser@gmail.com',
            subject = 'Test Subject',
            message = ''
        )
        self.assertTrue(isinstance(contact_us, Contact))

