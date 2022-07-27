import string
from django.db import models
from django.urls import reverse
from django.utils import timezone

from users.models import Usuario

EXPIRATION_DAYS = 10
DOMAIN = 'http://127.0.0.1:8000/'
# DOMAIN = 'http://192.168.0.102:8000/'
# DOMAIN = 'https://encurtalinks.com.br/'

def time_expiration():
    return timezone.now() + timezone.timedelta(days=EXPIRATION_DAYS)


class Link(models.Model):
    url = models.CharField(max_length=200)
    shortened_url = models.CharField(max_length=8, )
    created_by = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='created_by')
    data_creation = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=time_expiration, editable=False)

    def __str__(self):
        return f'{self.url}'

    def create_link(self, id):
        ''' Codifica 62 caracteres '''
        characters = string.digits + string.ascii_letters
        base = len(characters)

        result = []
        while id > 0:
            val = id % base
            result.append(characters[val])
            id = id // base

        return DOMAIN + ''.join(result[::-1])

    def save(self, *args, **kwargs):
        id_digits = int(1e8)
        last_link = Link.objects.last()
        try:
            last_id = last_link.id
        except AttributeError:
            last_id = 1

        self.shortened_url = self.create_link(last_id + id_digits)

        super(Link, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shortener:DashboardLink')