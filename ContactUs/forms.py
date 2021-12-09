from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Contact
from django.contrib.auth import get_user_model

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ("email", "subject", "message")
