from django.contrib.auth.models import AbstractUser, Group 
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

org_Choices = (
    ('GENERAL', 'General'),
    ('IT', 'Information Technology'),
    ('R&D', 'Research and Devleopment'),
    ('SECURITY', 'Security'),
    ('MARKETING', 'Marketing'),
    ('FINANCE', 'Finance'),
    ('HR', 'Human Resources'),
)

class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    display_name = models.CharField(verbose_name=("Display Name"), max_length=50, null=True, blank=True)
    date_of_birth = models.DateField(verbose_name=("Date of Birth"), null=True, blank=True)
    Organization_name = models.CharField(verbose_name=("Organization Name"), max_length=50, null=True, blank=True)
    Organization_type = models.CharField(verbose_name=("Organization Type"), max_length=50, null=True, blank=True)
    Organization_address = models.CharField(verbose_name=("Organization Address"), max_length=50, null=True, blank=True)
    Organization_city = models.CharField(verbose_name=("Organization City"), max_length=50, null=True, blank=True)
    Organization_state = models.CharField(verbose_name=("Organization State"), max_length=50, null=True, blank=True)
    Organization_zip = models.CharField(verbose_name=("Organization Zip"), max_length=50, null=True, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(verbose_name=("Phone Number"), validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    additional_info = models.TextField(verbose_name=("Additional Info"), max_length=500, null=True, blank=True)
    photo = models.ImageField(verbose_name=("Photo"), upload_to='photos/', default = 'photos/default.png', null=True, blank=True)
    Organizational_pin = models.CharField(verbose_name=("Organization Pin"), max_length=50, null=True, blank=True)
    Organizatoin_user_type = models.CharField(verbose_name=("Organization User Type"), max_length=50, choices=org_Choices, null=True, blank=True, default='GENERAL')

    class Meta:
        ordering = ('last_name',)
    def __str__(self):
        return f"{self.username}: "
        # {self.first_name} {self.last_name}  removed to test Username display