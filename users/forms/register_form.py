from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from utils.regex import strong_password
from users.models import Usuario
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible
from django.utils.translation import gettext_lazy as _


class UserAuthenticationForm(AuthenticationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)


class RegisterModelForm(forms.ModelForm):

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _("Type your name")}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _("Enter your Last Name")}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _("Type your e-mail")}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _("Type your password")}),
        help_text=(
            _('The password must have at least one uppercase letter, one lowercase letter and one number. Length must be at least 8 characters')
        ),
        validators=[strong_password]
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                     'placeholder': _("Type the password again")}))
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'password', 'is_staff', 'is_active', 'image']


    def clean(self):
        cleaned_data = super(RegisterModelForm, self).clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            password_confirmation_error = ValidationError(
                _('Password and Confirm Password must be the same'),
                code='invalid'
            )
            raise ValidationError({
                'confirm_password': password_confirmation_error
            })


class CadastroUsuarioModelForm(forms.ModelForm):

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _("Type your name")}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _("Enter your Last Name")}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _("Type your e-mail")}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _("Type your password")}),
        help_text=(
            _('The password must have at least one uppercase letter, one lowercase letter and one number. Length must be at least 8 characters')
        ),
        validators=[strong_password]
    )
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                     'placeholder': _("Type the password again")}))
    # imagem = forms.ImageField(widget=forms.TextInput(attrs={'class': 'custom-file-input', 'id': 'customFile'}))
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'password', 'is_staff', 'is_active', 'image']


    def clean(self):
        cleaned_data = super(CadastroUsuarioModelForm, self).clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            password_confirmation_error = ValidationError(
                _('Password and Confirm Password must be the same'),
                code='invalid'
            )
            raise ValidationError({
                'confirm_password': password_confirmation_error
            })


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _("Type your name")}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _("Enter your Last Name")}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _("Type your e-mail")}))


    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'is_staff', 'is_active', 'image']




class ViewUserModelForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled', 'placeholder': _("Type your name")}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled', 'placeholder': _("Enter your Last Name")}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'disabled': 'disabled', 'placeholder': _("Type your e-mail")}))
    image = forms.FileInput()
    is_active = forms.BooleanField(required=False,)
    is_active.widget.attrs['disabled'] = True
    is_staff = forms.BooleanField(required=False,)
    is_staff.widget.attrs['disabled'] = True
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'is_staff', 'is_active', 'image']