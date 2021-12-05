from django.views.generic import TemplateView
from django.shortcuts import render

def HomePageView(request):
    context = {}
    return render(request, 'home.html', context)

def ProfileView(request):
    context = {}
    return render(request, 'profile.html', context)

def AboutView(request):
    context = {}
    return render(request, 'about.html', context)

def AnnouncementsView(request):
    context = {}
    return render(request, 'announcements.html', context)
    
