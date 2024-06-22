from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'), # Esse template_name a gente nomeia para ser redirecionado para nossa tela de login, se não colocar, ele redicionará para tela de login padrão do Django
    
]
