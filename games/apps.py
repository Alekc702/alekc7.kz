from django.apps import AppConfig
import os
from django.db.models.signals import post_save
from django.dispatch import receiver


class GamesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'games'

    def ready(self):
        from .models import Game

        @receiver(post_save, sender=Game)
        def _fix_file_perms(sender, instance, **kwargs):
            if instance.cover and hasattr(instance.cover, 'path'):
                try:
                    # Ensure file is at least readable (644) and directory exists
                    os.makedirs(os.path.dirname(instance.cover.path), exist_ok=True)
                    os.chmod(instance.cover.path, 0o644)
                except Exception:
                    # Ignore permission errors on platforms where chmod isn't applicable
                    pass
    verbose_name = 'Игры'


