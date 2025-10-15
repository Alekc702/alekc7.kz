import os
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Ensure STATIC_ROOT and MEDIA_ROOT directories exist (create with safe permissions)'

    def handle(self, *args, **options):
        static_root = getattr(settings, 'STATIC_ROOT', None)
        media_root = getattr(settings, 'MEDIA_ROOT', None)

        created = []

        if static_root:
            os.makedirs(static_root, exist_ok=True)
            try:
                os.chmod(static_root, 0o755)
            except Exception:
                pass
            created.append(static_root)

        if media_root:
            os.makedirs(media_root, exist_ok=True)
            # Ensure default upload subdir exists
            try:
                os.makedirs(os.path.join(media_root, 'game_covers'), exist_ok=True)
            except Exception:
                pass
            try:
                os.chmod(media_root, 0o755)
            except Exception:
                pass
            created.append(media_root)

        if created:
            self.stdout.write(self.style.SUCCESS('Created/verified directories:'))
            for p in created:
                self.stdout.write(f" - {str(p)}")
        else:
            self.stdout.write(self.style.WARNING('STATIC_ROOT or MEDIA_ROOT not set in settings.'))
