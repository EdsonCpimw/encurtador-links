from django.shortcuts import render
from django.utils.decorators import method_decorator
from users.mixins import UsuarioMixin
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required


@method_decorator(login_required(login_url='login'), name='dispatch')
class HomeView(UsuarioMixin, TemplateView):
    template_name = 'home/home.html'

