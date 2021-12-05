from django.urls import path 
from .views import SignUpAdminView, SignUpEUView, ChooseUserTypeView, login_view, logout_view, PasswordChangeDoneView, PasswordChangeView, PasswordResetDoneView, PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView 

urlpatterns = [
    path('adminsignup/', SignUpAdminView, name='Adminsignup'),
    path('clienteusignup/', SignUpEUView, name='clienteusignup'),
    path('choosetype/', ChooseUserTypeView.as_view(), name='choosetype'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),


    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),


]