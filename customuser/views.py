from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .TokenLoginHandler import TokenLoginHandler
import logging
import time


from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationAdminForm, CustomUserCreationEUForm


logger = logging.getLogger(__name__)

#write to log file


# Create your views here.
def SignUpAdminView(request):
    sw = time.time()
    form = CustomUserCreationAdminForm
    tk = TokenLoginHandler()

    if request.method == 'POST':
        form = CustomUserCreationAdminForm(request.POST)
        if form.is_valid():
            org_name = form.cleaned_data.get('Organization_name')
            if (tk.token_found_compute(org_name) == False):
                tk.generate_token(org_name)
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                messages.success(request, 'Token generated for ' + org_name + ': ' + tk.generate_token(org_name))
                messages.success(request, 'TAKE NOTE OF THIS TOKEN: once you login, it will never be displayed again')
                messages.success(request, 'Use this token for end-user sign up to your organization')
                logger.info('Token generated for ' + org_name + ': ' + tk.generate_token(org_name) + ' in ' + str(round((time.time() - sw) * 1000, 4)) + ' ms')
                return redirect('login')
            else:
                logger.error('Token already exists for ' + org_name + ' found in ' + str(round((time.time() - sw) * 1000, 4)) + ' ms')
                return HttpResponse("Organization already exists, please contect support or use a different Oranizational Name.")
                
    context = {'form':form}
    return render(request, 'registration/adminsignup.html', context)

def SignUpEUView(request):
    sw = time.time()
    form = CustomUserCreationEUForm
    tk = TokenLoginHandler()

    if request.method == 'POST':
        form = CustomUserCreationEUForm(request.POST)
        if form.is_valid():
            org_pin = str(form.cleaned_data.get('Organizational_pin'))
            org_name = form.cleaned_data.get('Organization_name')
            if (tk.token_found_compute(org_name) == True and str(tk.generate_token(org_name)) == org_pin):
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                logger.info('Account was created for ' + user + ' in ' + str(round((time.time() - sw) * 1000, 4)) + ' ms')
                return redirect('login')
            else:
                messages.error(request, 'Organization does not exist, or you have entered the wrong token')
                logger.error('Organization did not excist, or they entered the wrong tokem ' + str(round((time.time() - sw) * 1000, 4)) + ' ms')
                return redirect('clienteusignup')

    context = {'form':form}
    return render(request, 'registration/client_EU_signup.html', context)

class ChooseUserTypeView(TemplateView):
    template_name = 'registration/choose_user_type.html'

def login_view(request):
    sw = time.time()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            logger.info('User ' + username + ' logged in: in ' + str(round((time.time() - sw) * 1000, 4)) + ' ms')
            login(request, user)
            return redirect('home')
        else:
            logger.error('User ' + username + ' failed to log in: in ' + str(round((time.time() - sw) * 1000, 4)) + ' ms')
            messages.info(request, 'Username or password is incorrect')
    context = []
    return render(request, 'registration/login.html')

def logout_view(request):
    sw = time.time()
    logger.info('User ' + request.user.username + ' logged out: in ' + str(round((time.time() - sw) * 1000, 4)) + ' ms')
    logout(request)
    return redirect('login')