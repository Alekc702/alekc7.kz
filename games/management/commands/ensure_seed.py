from django.core.management.base import BaseCommand
from django.core.management import call_command
from games.models import Game


class Command(BaseCommand):
    help = 'Seed initial data from fixtures/games_initial_data.json if no games exist.'

    def handle(self, *args, **options):
        if Game.objects.exists():
            self.stdout.write(self.style.WARNING('Games already exist; skipping seeding.'))
            return
        try:
            call_command('loaddata', 'fixtures/games_initial_data.json')
            self.stdout.write(self.style.SUCCESS('Initial games data loaded.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Failed to load initial data: {e}'))