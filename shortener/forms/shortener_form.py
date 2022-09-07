from django import forms
from shortener.models import Link
from users.models import Usuario
from django.utils.translation import gettext_lazy as _


class RegisterUrlModelForm(forms.ModelForm):

    url = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': _("Your URL here")}))
    shortened_url = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'disabled': True}))
    created_by = forms.ModelChoiceField(required=False, queryset=Usuario.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control  select2bs4', }))
    
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
        attrs={'class': 'form-control', 'placeholder': _("Your URL here"), 'disabled': True}))
    shortened_url = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'disabled': True}))
    created_by = forms.ModelChoiceField(required=False, queryset=Usuario.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control', 'disabled': True}))

    class Meta:
        model = Link
        fields = ['url', 'shortened_url', 'created_by']





class FilterForm(forms.Form):
    filter_choices = (
        ('', _('-----  Select  -----')),
        (1, _('All Links')),
        (2, _('Expired links')),
        (3, _('Links not expired')),
    )
    filter = forms.ChoiceField(choices=filter_choices, widget=forms.Select(
        attrs={'class': 'form-control'}))