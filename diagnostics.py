import os

# Ensure Django settings are loaded when running as a standalone script
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mylibrary.settings')
import django
django.setup()

from django.conf import settings
from django.db import connection

print('DATABASE NAME:', settings.DATABASES['default'].get('NAME'))

cur = connection.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cur.fetchall()
print('TABLES:', tables)

cur.execute("PRAGMA table_info('books_book');")
cols = cur.fetchall()
print("books_book columns:", cols)

# Show applied migrations for 'books' app
try:
    cur.execute("SELECT app, name FROM django_migrations WHERE app='books';")
    print('django_migrations for books:', cur.fetchall())
except Exception:
    print('django_migrations table not accessible')

try:
    from books.models import Book
    print('Book objects count:', Book.objects.count())
except Exception as e:
    print('Error importing Book or counting:', repr(e))
    
cur.execute("PRAGMA table_info('books_author');")
print('books_author columns:', cur.fetchall())
cur.execute("PRAGMA table_info('books_category');")
print('books_category columns:', cur.fetchall())
