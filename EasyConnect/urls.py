from django.urls import path
from .views import HomePageView, ProfileView

urlpatterns = [
   
    path('Home', HomePageView, name='home'),
    path('profile', ProfileView, name = 'profile'),

]