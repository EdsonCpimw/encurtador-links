import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from users.managers import UsuarioManager


def upload_image_user(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return "users/%s" % (filename)


class Usuario(AbstractUser):
    password = models.CharField(_('password'), max_length=128)
    email = models.EmailField('Email', unique=True)
    imagem = models.ImageField(upload_to=upload_image_user, blank=True)

    is_staff = models.BooleanField(
        _('admin status'),
        default=False,
        help_text=_(
            'Permite que o usuario possa fazer login na pagina de Administração.'),
    )

    is_superuser = models.BooleanField(
        _('super_user status'),
        default=False,
        help_text=_(
            'Permite ser um Super Usuário'),
    )

    objects = UsuarioManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',]

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
        db_table = 'tb_usuario'
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    # @property
    # def is_staff(self):
    #     return self.is_staff
    # @property
    # def is_superuser(self):
    #     return self.is_superuser