from django.urls import path
from .views import HomePageView, ProfileView

urlpatterns = [
    path('', HomePageView, name='home'),
    path('Home', HomePageView, name='home'),
    path('profile', ProfileView, name = 'profile'),

]