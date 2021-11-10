from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm 
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

class CustomUserCreationAdminForm(UserCreationForm):
    email = forms.EmailField(required=True)
    Organization_name = forms.CharField(required=True)
    class Meta(UserCreationForm):
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2', 'display_name', 'Organization_name', 'Organization_type', 'Organization_address', 'Organization_city', 'Organization_state', 'Organization_zip', 'additional_info', 'photo','Organizational_pin')

class CustomUserCreationEUForm(UserCreationForm):
    email = forms.EmailField(required=True)
    Organization_name = forms.CharField(required=True)
    Organizational_pin = forms.CharField(required=True)
    class Meta(UserCreationForm):
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2', 'display_name', 'Organization_name', 'additional_info', 'photo', 'Organizational_pin')
        
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = UserChangeForm.Meta.fields