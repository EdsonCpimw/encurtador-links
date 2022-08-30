from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse_lazy
from shortener.forms import RegisterUrlModelForm
from shortener.forms.shortener_form import ViewUrlModelForm, FilterForm
from shortener.models import Link, EXPIRATION_DAYS
from django.views.generic.edit import CreateView, DeleteView, ModelFormMixin
from django.views.generic import ListView, DetailView, FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from rolepermissions.mixins import HasPermissionsMixin
from utils.regex import remove_https
from django.utils.translation import gettext as _

from users.mixins import UsuarioMixin


class RedirectLink(View):

    def get(self, request, *args, **kwargs):
        now = timezone.now() + timezone.timedelta(days=EXPIRATION_DAYS)
        try:
            link = Link.objects.filter(expires_at__lt=now, shortened_url__contains=kwargs.get('link')).first()
            url = link.url
            if url:
                return redirect('//' + url)
        except:
            raise Http404

@method_decorator(login_required(login_url='login'), name='dispatch')
class CreationLinkView(HasPermissionsMixin, UsuarioMixin, CreateView):
    required_permission = 'Cadastrar_link'
    form_class = RegisterUrlModelForm
    template_name = 'shortener/criar_link.html'

    def get_form_kwargs(self):
        kwargs = super(CreationLinkView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form, *args, **kwargs):
        """TODO: domain atual só serve para ambiente local, mudar para ['SERVER_NAME'] em caso de deploy"""
        link = form.save(commit=False)
        link.shortened_url = ''
        link.url = remove_https(link.url)
        user = self.request.user
        link.domain = self.request.META['SERVER_NAME']
        if not user.is_staff:
            link.created_by = self.request.user
        messages.success(self.request, _(f'Link generated successfully'))
        return super(CreationLinkView, self).form_valid(form, *args, **kwargs)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, _('Error generating shortened link'))
        return super(CreationLinkView, self).form_invalid(form, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('shortener:Detail_link', kwargs={'pk': self.object.pk})


@method_decorator(login_required(login_url='login'), name='dispatch')
class LinksView(HasPermissionsMixin, UsuarioMixin, FormView, ListView):
    required_permission = 'listar_links'
    form_class = FilterForm
    template_name = 'shortener/lista_link.html'
    context_object_name = 'links'
    model = Link

    def filter_links(self, filter):
        now = timezone.now()
        if filter == '1':
            return Link.objects.all()
        if filter == '2':
            return Link.objects.filter(expires_at__lt=now)
        elif filter == '3':
            return Link.objects.filter(expires_at__gt=now)

    def get_queryset(self, *args, **kwargs):
        queryset = super(LinksView, self).get_queryset()
        data = self.request.GET
        filter = data.get('filter')
        now = timezone.now()
        user = self.request.user
        if user.is_staff and filter:
            links = self.filter_links(filter=filter)
        elif user.is_staff:
            links = queryset.all()
        else:
            links = queryset.filter(expires_at__gt=now, created_by=self.request.user)
        return links

@method_decorator(login_required(login_url='login'), name='dispatch')
class DeleteLinkView(HasPermissionsMixin, DeleteView):
    required_permission = 'deletar_link'
    sucess_message = _('Link successfully deleted!')


    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        link = get_object_or_404(Link, pk=pk)
        return link

    def get_success_url(self):
        return reverse_lazy('shortener:List_link')

@method_decorator(login_required(login_url='login'), name='dispatch')
class DetailLinkView(HasPermissionsMixin, UsuarioMixin, ModelFormMixin, DetailView):
    required_permission = 'detalhes_link'
    model = Link
    template_name = 'shortener/criar_link.html'
    # context_object_name = 'link'
    form_class = ViewUrlModelForm

@method_decorator(login_required(login_url='login'), name='dispatch')
class BulkDeleteLinksView(HasPermissionsMixin, View):
    required_permission = 'remover_links'
    model = Link
    success_url = reverse_lazy('shortener:List_link')

    def post(self, request, *args, **kwargs):
        now = timezone.now()
        try:
            links = Link.objects.filter(expires_at__lt=now)
            self.model.objects.filter(pk__in=links).delete()
            messages.success(request, _('All expired links were successfully removed!'))
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            messages.error(request, _(f'Unable to remove links: {type(e)}'))
            return HttpResponseRedirect(self.success_url)


