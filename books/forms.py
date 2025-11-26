from django import forms
from .models import Book, Author, Category


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description', 'category', 'authors', 'cover']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название книги'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание книги', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'authors': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
