from django.urls import path 
from .views import SignUpAdminView, SignUpEUView, ChooseUserTypeView, login_view, logout_view

urlpatterns = [
    path('adminsignup/', SignUpAdminView, name='Adminsignup'),
    path('clienteusignup/', SignUpEUView, name='clienteusignup'),
    path('choosetype/', ChooseUserTypeView.as_view(), name='choosetype'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]