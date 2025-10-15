from django.db import models
from django.urls import reverse


class Studio(models.Model):
    """Студия разработки игр"""
    name = models.CharField(max_length=200, verbose_name='Название')
    country = models.CharField(max_length=100, verbose_name='Страна')
    year_founded = models.IntegerField(verbose_name='Год основания')
    
    class Meta:
        verbose_name = 'Студия'
        verbose_name_plural = 'Студии'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Engine(models.Model):
    """Игровой движок"""
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    
    class Meta:
        verbose_name = 'Движок'
        verbose_name_plural = 'Движки'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Platform(models.Model):
    """Игровая платформа"""
    name = models.CharField(max_length=100, verbose_name='Название')
    
    class Meta:
        verbose_name = 'Платформа'
        verbose_name_plural = 'Платформы'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Game(models.Model):
    """Игра"""
    title = models.CharField(max_length=300, verbose_name='Название')
    release_year = models.IntegerField(verbose_name='Год выпуска')
    description = models.TextField(verbose_name='Описание разработки')
    studio = models.ForeignKey(
        Studio, 
        on_delete=models.CASCADE, 
        related_name='games',
        verbose_name='Студия'
    )
    engine = models.ForeignKey(
        Engine, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='games',
        verbose_name='Движок'
    )
    platforms = models.ManyToManyField(
        Platform, 
        related_name='games',
        verbose_name='Платформы'
    )
    cover = models.ImageField(
        upload_to='game_covers/', 
        null=True, 
        blank=True,
        verbose_name='Обложка/Скриншот'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'
        ordering = ['-release_year', 'title']
    
    def __str__(self):
        return f"{self.title} ({self.release_year})"
    
    def get_absolute_url(self):
        return reverse('game_detail', args=[str(self.id)])


