from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = 'home.html'

class ProfileView(TemplateView):
    template_name = 'profile.html'
    
