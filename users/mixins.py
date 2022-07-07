class UsuarioMixin(object):
    
    def get_context_data(self, **kwargs):
        usuario = self.request.user
        context = super(UsuarioMixin, self).get_context_data(**kwargs)
        context['usuarioLogado'] = usuario
        return context