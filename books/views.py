from django.shortcuts import render, get_object_or_404
from .models import Book, Author, Category


def books_index(request):
    """Список всех книг с фильтрами по автору и категории."""
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


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'books/detail.html', {'book': book})
