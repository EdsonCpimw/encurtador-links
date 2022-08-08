import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
    if not regex.match(password):
        raise ValidationError((
            _('The password must contain uppercase, lowercase, numbers and at least 8 characters')
        ))

def remove_https(url):
    link = re.compile(r"https?://(www\.)?")
    return link.sub('', url).strip().strip('/')