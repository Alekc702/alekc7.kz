from django import forms
from .models import Game, Studio, Engine, Platform


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'release_year', 'description', 'studio', 'engine', 'platforms', 'cover']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название игры'}),
            'release_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Год выпуска'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Описание разработки игры',
                'rows': 5
            }),
            'studio': forms.Select(attrs={'class': 'form-control'}),
            'engine': forms.Select(attrs={'class': 'form-control'}),
            'platforms': forms.CheckboxSelectMultiple(),
        }


class StudioForm(forms.ModelForm):
    class Meta:
        model = Studio
        fields = ['name', 'country', 'year_founded']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название студии'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Страна'}),
            'year_founded': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Год основания'}),
        }

