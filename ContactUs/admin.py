from django.contrib import admin
from .models import Contact

@admin.register(Contact)
class RequestDemoAdmin(admin.ModelAdmin):
  list_display = ['email', 'subject', 'message']