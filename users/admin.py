from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from users.models import Usuario

class EmployeeAdmin(UserAdmin):
    pass


admin.site.register(Usuario, EmployeeAdmin)