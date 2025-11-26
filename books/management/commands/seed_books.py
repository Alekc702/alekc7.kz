from django.core.management.base import BaseCommand
from django.db import transaction
from books.models import Author, Category, Book


class Command(BaseCommand):
    help = 'Seed books/authors/categories. Removes existing authors and categories first.'

    def add_arguments(self, parser):
        parser.add_argument('--no-reset', action='store_true', help='Do not delete existing authors/categories')

    def handle(self, *args, **options):
        reset = not options.get('no_reset')

        with transaction.atomic():
            if reset:
                self.stdout.write('Removing existing authors and categories...')
                Author.objects.all().delete()
                Category.objects.all().delete()

            # Create requested categories
            cat_history = Category.objects.create(name='история создания')
            cat_lore = Category.objects.create(name='лор')

            # Create requested authors
            author_harald = Author.objects.create(name='Харальд Хорф')
            author_kushner = Author.objects.create(name='Кушнер Дэвид')

            # Create books
            # Atomic Heart (no author provided) — add without authors and with a short placeholder description
            atomic = Book.objects.create(
                title='Atomic Heart',
                description='Atomic Heart — добавлено через seed script.',
                category=cat_lore
            )

            pred = Book.objects.create(
                title='Предыстория Предприятия 3826',
                description='Предыстория Предприятия 3826 — добавлено через seed script.',
                category=cat_history
            )
            pred.authors.add(author_harald)

            doom = Book.objects.create(
                title='Повелители DOOM',
                description='Повелители DOOM — добавлено через seed script.',
                category=cat_lore
            )
            doom.authors.add(author_kushner)

            self.stdout.write(self.style.SUCCESS('Seeding complete.'))
            self.stdout.write(f'Authors: {Author.objects.count()}, Categories: {Category.objects.count()}, Books: {Book.objects.count()}')
