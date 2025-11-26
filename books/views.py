from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Book, Author, Category
from .forms import BookForm


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


@login_required
def book_create(request):
    """Создание новой книги через сайт (только для авторизованных пользователей)."""
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm()

    context = {'form': form, 'action': 'Создать'}
    return render(request, 'books/form.html', context)
