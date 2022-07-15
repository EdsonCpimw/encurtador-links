from django import forms
from django.core.exceptions import ValidationError
from utils.regex import strong_password
from users.models import Usuario


class RegistroModelForm(forms.ModelForm):

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Digite seu Nome"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Digite seu Sobrenome"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "Digite seu Email"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Digite sua Senha"}),
        help_text=(
            'A senha deve ter pelo menos uma letra maiuscula, uma letra minuscula e um numero. O comprimento deve ser de pelo menos 8 caracteres'
        ),
        validators=[strong_password]
    )
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                     'placeholder': "Digite a senha novamente"}))
    # imagem = forms.ImageField(widget=forms.TextInput(attrs={'class': 'custom-file-input', 'id': 'customFile'}))
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'password', 'is_staff', 'is_active', 'imagem']


    def clean(self):
        cleaned_data = super(RegistroModelForm, self).clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            password_confirmation_error = ValidationError(
                'Senha e Confirma Senha precisam ser iguais',
                code='invalid'
            )
            raise ValidationError({
                'confirm_password': password_confirmation_error
            })


    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data['password'])
    #     user.username = self.cleaned_data['email']
    #     user.email = self.cleaned_data['email']
    #     if commit:
    #         user.save()
    #     return user


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Digite seu Nome"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Digite seu Sobrenome"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "Digite seu Email"}))


    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'is_staff', 'is_active', 'imagem']




class ViewUserModelForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled', 'placeholder': "Digite seu Nome"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled', 'placeholder': "Digite seu Sobrenome"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'disabled': 'disabled', 'placeholder': "Digite seu Email"}))
    imagem = forms.FileInput()
    is_active = forms.BooleanField(required=False,)
    is_active.widget.attrs['disabled'] = True
    is_staff = forms.BooleanField(required=False,)
    is_staff.widget.attrs['disabled'] = True
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'is_staff', 'is_active', 'imagem']