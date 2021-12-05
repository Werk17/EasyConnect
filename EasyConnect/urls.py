from django.urls import path
from .views import AboutView, AnnouncementsView, HomePageView, ProfileView

urlpatterns = [
    path('', HomePageView, name='home'),
    path('Home', HomePageView, name='home'),
    path('profile', ProfileView, name = 'profile'),
    path('about', AboutView, name='about'),
    path('announcements', AnnouncementsView, name='announcements'),

]