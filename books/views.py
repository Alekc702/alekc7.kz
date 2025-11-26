from django.shortcuts import render, get_object_or_404
import os
import traceback
from .models import Book, Author, Category


def books_index(request):
    """Список всех книг с фильтрами по автору и категории."""
    try:
        books = Book.objects.all().select_related('category').prefetch_related('authors')

        author_filter = request.GET.get('author')
        category_filter = request.GET.get('category')

        if author_filter:
            books = books.filter(authors__id=author_filter)
        if category_filter:
            books = books.filter(category_id=category_filter)

        context = {
            'books': books,
            'book_authors': Author.objects.all(),
            'book_categories': Category.objects.all(),
            'selected_author': author_filter,
            'selected_category': category_filter,
        }
        return render(request, 'books/index.html', context)
    except Exception:
        # Temporary debugging: print full traceback to stdout so Render logs capture it.
        tb = traceback.format_exc()
        print('\n--- BOOKS VIEW ERROR TRACEBACK ---\n', tb, flush=True)
        # Also write to a temp file for manual inspection if needed
        try:
            with open('/tmp/books_view_error.log', 'a', encoding='utf-8') as f:
                f.write(tb + '\n')
        except Exception:
            pass
        # If DEBUG_BOOKS env var set to '1', return traceback in response (temporary)
        if os.getenv('DEBUG_BOOKS') == '1':
            from django.http import HttpResponse
            return HttpResponse('<pre>' + tb.replace('<', '&lt;') + '</pre>', status=500)
        # Otherwise return generic 500 response
        from django.http import HttpResponseServerError
        return HttpResponseServerError('Internal Server Error — details logged on server.')


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'books/detail.html', {'book': book})
