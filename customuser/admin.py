from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm 
from .models import CustomUser

class CustomUserAdmin(UserAdmin): 
    add_form = CustomUserCreationForm 
    form = CustomUserChangeForm 
    model = CustomUser
    list_display = ['email', 'username', 'age', 'is_staff', 'Organization_name', 'display_name']
    fieldsets = UserAdmin.fieldsets + (
        ('Personal Information' , {'fields': ('age', 'date_of_birth', 'phone_number', )}),
        ('Organizational Information', {'fields': ('display_name', 'Organization_name', 'Organization_type', 'Organization_address', 'Organization_city', 'Organization_state', 'Organization_zip', 'additional_info', 'photo',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Personal Information' , {'fields': ('age', 'date_of_birth', 'phone_number', )}),
        ('Organizational Information', {'fields': ('display_name', 'Organization_name', 'Organization_type', 'Organization_address', 'Organization_city', 'Organization_state', 'Organization_zip', 'additional_info', 'photo',)}),
    )
admin.site.register(CustomUser, CustomUserAdmin)
