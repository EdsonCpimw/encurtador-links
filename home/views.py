from django.shortcuts import render
from users.mixins import UsuarioMixin
from django.views.generic.base import TemplateView

# Create your views here.

# class LoginView(TemplateView):
#     template_name = 'users/registration/login.html'

class HomeView(UsuarioMixin, TemplateView):
    template_name = 'home/home.html'