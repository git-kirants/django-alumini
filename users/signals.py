from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(pre_save, sender=User)
def set_admin_user_type(sender, instance, **kwargs):
    if instance.is_superuser and not instance.pk:  # Only for new superuser creation
        instance.user_type = 'admin' 