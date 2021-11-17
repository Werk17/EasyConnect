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
from django.contrib.auth.models import Group, GroupManager, PermissionsMixin 
from .forms import CustomUserChangeForm, CustomUserCreationAdminForm, CustomUserCreationEUForm


logger = logging.getLogger(__name__)

#write to log file


# Create your views here.
def SignUpAdminView(request):
    sw = time.time()
    form = CustomUserCreationAdminForm
    tk = TokenLoginHandler()
    p = loggingReports()
    groups = ['IT', 'GENERAL', 'HR', 'SECURITY', 'MARKETING', 'FINANCE', 'R&D']

    if request.method == 'POST':

        form = CustomUserCreationAdminForm(request.POST)

        if form.is_valid():

            if (tk.token_found_compute(form.cleaned_data.get('Organization_name')) == False):
                tk.generate_token(form.cleaned_data.get('Organization_name'))
                
                try:
                    AddUserToGroup(groups, Org_name_CleanUP(request.POST.get('Organization_name')), form, True)

                finally:
                    FormSaveandAccountCreation(form, Org_name_CleanUP(request.POST.get('Organization_name')), sw, request, tk, True)
                    return redirect('login')

            else:
                p.AdminLogging(form, sw)
                return HttpResponse("Organization already exists, please contect support or use a different Oranizational Name.")
                
    context = {'form':form}
    return render(request, 'registration/adminsignup.html', context)

def SignUpEUView(request):
    sw = time.time()
    form = CustomUserCreationEUForm
    tk = TokenLoginHandler()
    p = loggingReports()
    groups = ['IT', 'GENERAL', 'HR', 'SECURITY', 'MARKETING', 'FINANCE', 'R&D']

    if request.method == 'POST':
        form = CustomUserCreationEUForm(request.POST)
        if form.is_valid():

            if (tk.token_found_compute(form.cleaned_data.get('Organization_name')) == True and str(tk.generate_token(form.cleaned_data.get('Organization_name'))) == str(form.cleaned_data.get('Organizational_pin'))):

                try:
                    AddUserToGroup(groups, Org_name_CleanUP(form.cleaned_data.get('Organization_name')), form, False, request.POST.get('Organizatoin_user_type'))
                
                finally:
                    FormSaveandAccountCreation(form, Org_name_CleanUP(form.cleaned_data.get('Organization_name')), sw, request, tk, False)
                    p.EULogging(form.cleaned_data.get('username'), sw, "creation")
                    return redirect('login')

            else:
                messages.error(request, 'Organization does not exist, or you have entered the wrong token')
                p.EULogging(form.cleaned_data.get('username'), sw, "org_error")
                return redirect('clienteusignup')

    context = {'form':form}
    return render(request, 'registration/client_EU_signup.html', context)

class ChooseUserTypeView(TemplateView):
    template_name = 'registration/choose_user_type.html'

def login_view(request):
    sw = time.time()
    p = loggingReports()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            p.LoginGeneral(username, sw, "success")
            login(request, user)
            return redirect('home')
        else:
            p.LoginGeneral(username, sw, "failure")
            messages.info(request, 'Username or password is incorrect')
    context = []
    return render(request, 'registration/login.html')

def logout_view(request):
    sw = time.time()
    p = loggingReports()
    logout(request)
    p.LogoutGeneral(request, sw)
    return redirect('login')

#function to save the form and create the account
def FormSaveandAccountCreation(formsdata, org_name, sw, request, tk, is_admin):
    if is_admin == True:
        formsdata.save()
        username = formsdata.cleaned_data.get('username')
        messages.success(request, 'Account was created for ' + username)
        messages.success(request, 'Token generated for ' + org_name + ': ' + tk.generate_token(org_name))
        messages.success(request, 'TAKE NOTE OF THIS TOKEN: once you login, it will never be displayed again')
        messages.success(request, 'Use this token for end-user sign up to your organization')
        logger.info('Token generated for ' + org_name + ': ' + tk.generate_token(org_name) + ' in ' + str(round((time.time() - sw) * 1000, 4)) + ' ms')
    else:
        formsdata.save()
        user = formsdata.cleaned_data.get('username')
        messages.success(request, 'Account was created for ' + user)

#function to add user to group
def AddUserToGroup(groupsdict, org_nameuser, formsdata, is_admin, org_user_type):
    if is_admin == True:
        for i in groupsdict:
            user = formsdata.save(commit=False)
            user.save()
            group = Group.objects.create(name=org_nameuser + '_' + i)
            group = Group.objects.get(name=org_nameuser + '_' + i)
            user.groups.add(group)
    else:
        for i in groupsdict:
            if i.lower() == org_user_type.lower() or i.lower() == 'general':
                user = formsdata.save(commit=False)
                user.save()
                group = Group.objects.get(name=org_nameuser + '_' + i)
                user.groups.add(group)
            else:
                continue

# function to clean up the organization name
def Org_name_CleanUP(org_name):
    org_name = str(org_name)
    org_name = org_name.replace(" ", "").lower()
    return org_name

#private class to handle all the logging.
class loggingReports:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def AdminLogging(self, form, sw):
        self.logger.error('Token already exists for ' + form.cleaned_data.get('Organization_name') + ' found in ' + str(round((time.time() - sw) * 1000, 4)) + ' ms')
        return

    def LogoutGeneral(self, request, stopwatch):
        self.logger.info('User ' + request.user.username + ' logged out: in ' + str(round((time.time() - stopwatch) * 1000, 4)) + ' ms')
        return

    def EULogging(self, user, sw, info):
        if info == "org_error":
            logger.error('Organization did not excist, or they entered the wrong tokem ' + str(round((time.time() - sw) * 1000, 4)) + ' ms')
            return

        if info == "creation":
            logger.info('Account was created for ' + user + ' in ' + str(round((time.time() - sw) * 1000, 4)) + ' ms')
            return

    def LoginGeneral(self, username, sw, info):
        if info == "success":
            logger.info('User ' + username + ' logged in: in ' + str(round((time.time() - sw) * 1000, 4)) + ' ms')
            return
        if info == "failure":
            logger.error('User ' + username + ' failed to log in: in ' + str(round((time.time() - sw) * 1000, 4)) + ' ms')
            return
        
