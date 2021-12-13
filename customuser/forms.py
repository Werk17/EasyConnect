from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm 
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, User
import logging

logging = logging.getLogger(__name__)

class CustomUserCreationAdminForm(UserCreationForm):
    email = forms.EmailField(required=True)
    Organization_name = forms.CharField(required=True)
    class Meta(UserCreationForm):
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'phone_number', 'email', 'password1', 'password2', 'display_name', 'Organization_name', 'Organization_type', 'Organization_address', 'Organization_city', 'Organization_state', 'Organization_zip', 'additional_info', 'photo','Organizational_pin')
        logging.info("Forms added for Custom User Creation Admin Form")

class CustomUserCreationEUForm(UserCreationForm):
    email = forms.EmailField(required=True)
    Organization_name = forms.CharField(required=True)
    Organizational_pin = forms.CharField(required=True)
    class Meta(UserCreationForm):
        model = get_user_model()
        fields = ('username','first_name', 'last_name', 'phone_number', 'email', 'password1', 'password2', 'display_name', 'Organization_name', 'additional_info', 'photo', 'Organizational_pin', 'Organizatoin_user_type')
        logging.info("Forms added for Custom User Creation EU Form")
        
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = UserChangeForm.Meta.fields
        logging.info("Forms added for Custom User Change Form")