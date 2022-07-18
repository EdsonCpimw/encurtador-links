from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Usuario
from rolepermissions.roles import assign_role


@receiver(post_save, sender=Usuario)
def set_permissions(sender, instance, created, **kwargs):
    if created:
        if instance.is_staff == True:
            assign_role(instance, 'administrador')
        elif instance.is_staff == False:
            assign_role(instance, 'usuario')

