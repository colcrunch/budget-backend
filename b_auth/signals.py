import logging

from django.contrib.auth.models import User
from .models import UserProfile

from django.dispatch import receiver
from django.db.models.signals import post_save

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def create_required_model(sender, instance, created, *args, **kwargs):
    if created:
        logger.debug(f'User {instance} created. Creating default UserProfile.')
        UserProfile.objects.get_or_create(user=instance)
