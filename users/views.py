from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin
from users.forms import UserUpdateForm, ViewUserModelForm, UserAuthenticationForm, RegisterModelForm, \
    CadastroUsuarioModelForm
from users.mixins import UsuarioMixin
from users.models import Usuario
from rolepermissions.mixins import HasPermissionsMixin
from django.utils.translation import gettext as _


class LoginUserView(LoginView):
    form_class = UserAuthenticationForm


class RegisterUsuarioView(CreateView):
    form_class = RegisterModelForm
    template_name = 'registration/register_usuario.html'

    def form_valid(self, form, *args, **kwargs):
        user = form.save(commit=False)
        user.username = user.email
        user.set_password(user.password)
        user.is_active = True
        messages.success(self.request, _(f'User {user.username} successfully registered.'))
        return super(RegisterUsuarioView, self).form_valid(form,  *args, **kwargs)

    def form_invalid(self, form,  *args, **kwargs):
        messages.error(self.request, _('Error registering user'))
        return super(RegisterUsuarioView, self).form_invalid(form,  *args, **kwargs)

    def get_success_url(self):
       return reverse_lazy('login')


@method_decorator(login_required(login_url='login'), name='dispatch')
class UsuariosView(HasPermissionsMixin, UsuarioMixin, ListView):
    required_permission = 'listar_usuario'
    model = Usuario
    template_name = 'users/lista_usuario.html'
    # queryset = Usuario.objects.all()
    context_object_name = 'usuarios'
    # paginate_by = 10

    def get_queryset(self):
        usuarios = Usuario.objects.all()
        for user in usuarios:
            if user.is_active == True:
                 user.is_active =_('Active')
            else:
                 user.is_active =_('Inactive')
        return usuarios


@method_decorator(login_required(login_url='login'), name='dispatch')
class CadastroUsuarioView(HasPermissionsMixin, UsuarioMixin, SuccessMessageMixin, CreateView):
    required_permission = 'Cadastrar_usuario'
    form_class = CadastroUsuarioModelForm
    template_name = 'users/cadastro_usuario.html'
    # success_message = 'Usuário cadastrado com sucesso.'
    # success_url = reverse_lazy('users:Usuarios')

    def form_valid(self, form, *args, **kwargs):
        user = form.save(commit=False)
        user.username = user.email
        user.set_password(user.password)
        messages.success(self.request, _('User registered successfully.'))
        return super(CadastroUsuarioView, self).form_valid(form,  *args, **kwargs)

    def form_invalid(self, form,  *args, **kwargs):
        messages.error(self.request, _('Error registering user'))
        return super(CadastroUsuarioView, self).form_invalid(form,  *args, **kwargs)

    def get_success_url(self):
       return reverse_lazy('users:Usuarios')


@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdateUsuarioView(HasPermissionsMixin, UsuarioMixin, UpdateView):
    required_permission = 'Atualizar_usuario'
    form_class = UserUpdateForm
    #fields = ['first_name', 'last_name', 'email', 'administrador', 'is_active', 'imagem']
    template_name = 'users/cadastro_usuario.html'
    # success_url = reverse_lazy('users:Update_usuario')

    def get_object(self, queryset=None):
        usuario, created = Usuario.objects.update_or_create(id=self.kwargs['pk'])
        if self.request.user.is_active and self.request.user.is_staff:
            return usuario
        else:
            if self.request.user.id == self.kwargs['pk']:
                return usuario
            else:
                raise PermissionDenied


    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = user.email
        messages.success(self.request, _('User successfully updated.'))
        return super(UpdateUsuarioView, self).form_valid(form)

    def form_invalid(self, form,  *args, **kwargs):
        # messages.error(self.request, 'Erro ao atualizar usuário')
        return super(UpdateUsuarioView, self).form_invalid(form,  *args, **kwargs)

    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse_lazy('users:Usuarios')
        else:
            return reverse_lazy('users:Update_usuario', kwargs={'pk': self.request.user.id})


def delete_usuario_view(request, pk):
    """TODO: Necessário fazer um tratamento de error"""
    user = Usuario.objects.get(pk=pk)
    user.delete()
    messages.success(request, _("User successfully deleted!"))
    return redirect('users:Usuarios')


@method_decorator(login_required(login_url='login'), name='dispatch')
class DeleteUsuarioView(HasPermissionsMixin, SuccessMessageMixin, DeleteView):
    required_permission = 'deletar_usuario'
    success_url = reverse_lazy('users:Usuarios')
    success_message = _('User successfully deleted!')

    def get_object(self, queryset=None):
        id = self.kwargs.get('pk')
        user = get_object_or_404(Usuario, pk=id)
        return user


@method_decorator(login_required(login_url='login'), name='dispatch')
class DetailUserView(HasPermissionsMixin, UsuarioMixin, FormMixin, DetailView):
    required_permission = 'detalhes_usuario'
    queryset = Usuario.objects.all()
    template_name = 'users/user_detail.html'
    form_class = ViewUserModelForm

    def get_form(self, form_class=None):
        form = self.form_class(instance=self.object)
        return form
