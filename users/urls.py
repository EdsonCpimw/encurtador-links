from django.contrib import admin
from django.urls import path
from .views import (HomeView,
                    UsuariosView,
                    CadastroUsuarioView,
                    UpdateUsuarioView,
                    DeleteUsuarioView,
                    DetailUserView, )

app_name = 'users'

urlpatterns = [

    path('', UsuariosView.as_view(), name='Usuarios'),
    path('add/', CadastroUsuarioView.as_view(), name='Cadastro_usuario'),
    path('<int:pk>/update/', UpdateUsuarioView.as_view(), name='Update_usuario'),
    path('<int:pk>/delete/', DeleteUsuarioView.as_view(), name='Delete_usuario'),
    path('<int:pk>/detail/', DetailUserView.as_view(), name='usuario_Detail'),
]
