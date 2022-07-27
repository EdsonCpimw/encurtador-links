from django import forms
from shortener.models import Link
from users.models import Usuario


class RegisterUrlModelForm(forms.ModelForm):

    url = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Seu URL aqui"}))
    shortened_url = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'disabled': True}))
    created_by = forms.ModelChoiceField(required=False, queryset=Usuario.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control', 'id': 'select2'}))
    
    class Meta:
        model = Link
        fields = ['url', 'shortened_url', 'created_by']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(RegisterUrlModelForm, self).__init__(*args, **kwargs)
        if self.user.is_staff:
            self.fields['created_by'].required = True


class ViewUrlModelForm(forms.ModelForm):
    url = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Seu URL aqui", 'disabled': True}))
    shortened_url = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'disabled': True}))
    created_by = forms.ModelChoiceField(required=False, queryset=Usuario.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control', 'disabled': True}))

    class Meta:
        model = Link
        fields = ['url', 'shortened_url', 'created_by']





class FilterForm(forms.Form):
    filter_choices = (
        ('', '-----  Selecione  -----'),
        (1, 'Todos os Links'),
        (2, 'Links expirado'),
        (3, 'Links não expirado'),
    )
    filter = forms.ChoiceField(choices=filter_choices, widget=forms.Select(attrs={'class': 'form-control'}))