from django.urls import path
from .views import HomePageView, ProfileView

urlpatterns = [
   
    path('', HomePageView.as_view(), name='home'),
    path('profile/', ProfileView.as_view(), name = 'profile'),

]