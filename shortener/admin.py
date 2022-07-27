from django.contrib import admin

# Register your models here.
from shortener.models import Link

admin.site.register(Link)