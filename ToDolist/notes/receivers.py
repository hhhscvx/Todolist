from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.core.cache import cache
from django.conf import settings
from .services.cache_delete import cache_delete


@receiver(user_logged_out)  # при логауте выполнять эту func
def clear_cache_on_logout(sender, request, user, **kwargs):
    cache_delete(cache, settings)
