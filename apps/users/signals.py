# using 'post_save' signal for User model to notify creation of a Profile
# model, due to the fact that we also have the admin app able to create users.

import string
import random
from .models import User, Profile
from apps.apibroker.models import UserCase
from django.dispatch import receiver
from django.db.models.signals import post_save

def random_choice():
    alphabet = string.ascii_lowercase + string.digits
    return ''.join(random.choices(alphabet, k=8))
    
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()