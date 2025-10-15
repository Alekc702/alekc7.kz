from django.contrib import admin
from .models import Game, Studio, Engine, Platform


@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'year_founded')
    list_filter = ('country', 'year_founded')
    search_fields = ('name', 'country')
    ordering = ('name',)


@admin.register(Engine)
class EngineAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'description')
    ordering = ('name',)


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_year', 'studio', 'engine', 'created_at')
    list_filter = ('release_year', 'studio', 'engine', 'platforms')
    search_fields = ('title', 'description', 'studio__name')
    filter_horizontal = ('platforms',)
    ordering = ('-release_year', 'title')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'release_year', 'description')
        }),
        ('Разработка', {
            'fields': ('studio', 'engine', 'platforms')
        }),
        ('Медиа', {
            'fields': ('cover',)
        }),
    )

