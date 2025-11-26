from django.db import models
from django.urls import reverse


class Author(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя автора')

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Категория')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    """Модель книги, согласованная со схемой текущей базы данных."""
    title = models.CharField(max_length=300, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    cover = models.ImageField(upload_to='book_covers/', null=True, blank=True, verbose_name='Обложка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    # Связи (в базе уже существуют соответствующие таблицы)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books',
        verbose_name='Категория'
    )
    authors = models.ManyToManyField(Author, related_name='books', verbose_name='Авторы')

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['-created_at', 'title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_detail', args=[str(self.id)])
