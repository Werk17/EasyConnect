from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .TokenLoginHandler import TokenLoginHandler
import logging
import time


from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, UserModel
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group, Permission, User
from .forms import CustomUserChangeForm, CustomUserCreationAdminForm, CustomUserCreationEUForm

from urllib.parse import urlparse, urlunparse

from django.conf import settings
# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import (
    url_has_allowed_host_and_scheme, urlsafe_base64_decode,
)
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import permission_required


logger = logging.getLogger(__name__)

#write to log file
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
                    AddUserToGroup(groups, Org_name_CleanUP(request.POST.get('Organization_name')), form, True, "")

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
        formsdata.instance.is_staff = True
        formsdata.instance.user_permissions.add(Permission.objects.get(name='Can add group'))
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
            logger.info('Adding user to group ' + i + ' in ' + org_nameuser)
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

class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            **(self.extra_context or {})
        })
        return context


class PasswordResetView(PasswordContextMixin, FormView):
    email_template_name = 'registration/password_reset_email.html'
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    template_name = 'registration/password_reset_form.html'
    title = _('Password reset')
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)


INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'


class PasswordResetDoneView(PasswordContextMixin, TemplateView):
    template_name = 'registration/password_reset_done.html'
    title = _('Password reset sent')


class PasswordResetConfirmView(PasswordContextMixin, FormView):
    form_class = SetPasswordForm
    post_reset_login = False
    post_reset_login_backend = None
    reset_url_token = 'set-password'
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'registration/password_reset_confirm.html'
    title = _('Enter new password')
    token_generator = default_token_generator

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        if 'uidb64' not in kwargs or 'token' not in kwargs:
            raise ImproperlyConfigured(
                "The URL path must contain 'uidb64' and 'token' parameters."
            )

        self.validlink = False
        self.user = self.get_user(kwargs['uidb64'])

        if self.user is not None:
            token = kwargs['token']
            if token == self.reset_url_token:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, display the password reset form.
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(token, self.reset_url_token)
                    return HttpResponseRedirect(redirect_url)

        # Display the "Password reset unsuccessful" page.
        return self.render_to_response(self.get_context_data())

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist, ValidationError):
            user = None
        return user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        if self.post_reset_login:
            auth_login(self.request, user, self.post_reset_login_backend)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.validlink:
            context['validlink'] = True
        else:
            context.update({
                'form': None,
                'title': _('Password reset unsuccessful'),
                'validlink': False,
            })
        return context


class PasswordResetCompleteView(PasswordContextMixin, TemplateView):
    template_name = 'registration/password_reset_complete.html'
    title = _('Password reset complete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url(settings.LOGIN_URL)
        return context


class PasswordChangeView(PasswordContextMixin, FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'registration/password_change_form.html'
    title = _('Password change')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)


class PasswordChangeDoneView(PasswordContextMixin, TemplateView):
    template_name = 'registration/password_change_done.html'
    title = _('Password change successful')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
        
