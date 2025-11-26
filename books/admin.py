from django.contrib import admin
from .models import Book, Author, Category


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    def get_authors(self, obj):
        return ', '.join(str(a) for a in obj.authors.all())
    get_authors.short_description = 'Авторы'

    list_display = ('title', 'get_authors', 'category', 'created_at')
    search_fields = ('title', 'authors__name')
    list_filter = ('category',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
