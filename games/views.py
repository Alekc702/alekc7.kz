from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Game, Studio, Engine, Platform
from .utils import api_key_required
from .forms import GameForm, StudioForm


def index(request):
    """Главная страница со списком игр"""
    games = Game.objects.all().select_related('studio', 'engine').prefetch_related('platforms')
    
    # Фильтрация
    studio_filter = request.GET.get('studio')
    engine_filter = request.GET.get('engine')
    year_filter = request.GET.get('year')
    
    if studio_filter:
        games = games.filter(studio_id=studio_filter)
    if engine_filter:
        games = games.filter(engine_id=engine_filter)
    if year_filter:
        games = games.filter(release_year=year_filter)
    
    context = {
        'games': games,
        'studios': Studio.objects.all(),
        'engines': Engine.objects.all(),
        'years': Game.objects.values_list('release_year', flat=True).distinct().order_by('-release_year'),
    }
    return render(request, 'games/index.html', context)


def game_detail(request, pk):
    """Детальная страница игры"""
    game = get_object_or_404(Game.objects.select_related('studio', 'engine').prefetch_related('platforms'), pk=pk)
    context = {'game': game}
    return render(request, 'games/detail.html', context)


@login_required
def game_create(request):
    """Создание новой игры"""
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            game = form.save()
            return redirect('game_detail', pk=game.pk)
    else:
        form = GameForm()
    
    context = {'form': form, 'action': 'Создать'}
    return render(request, 'games/form.html', context)


@login_required
def game_update(request, pk):
    """Редактирование игры"""
    game = get_object_or_404(Game, pk=pk)
    
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES, instance=game)
        if form.is_valid():
            form.save()
            return redirect('game_detail', pk=game.pk)
    else:
        form = GameForm(instance=game)
    
    context = {'form': form, 'action': 'Редактировать', 'game': game}
    return render(request, 'games/form.html', context)


@login_required
def game_delete(request, pk):
    """Удаление игры"""
    game = get_object_or_404(Game, pk=pk)
    
    if request.method == 'POST':
        game.delete()
        return redirect('index')
    
    context = {'game': game}
    return render(request, 'games/confirm_delete.html', context)


# API Endpoints
@api_key_required
def api_games_list(request):
    """API: Список всех игр в формате JSON"""
    games = Game.objects.all().select_related('studio', 'engine').prefetch_related('platforms')
    
    data = [{
        'id': game.id,
        'title': game.title,
        'release_year': game.release_year,
        'description': game.description,
        'studio': {
            'id': game.studio.id,
            'name': game.studio.name,
            'country': game.studio.country,
            'year_founded': game.studio.year_founded
        } if game.studio else None,
        'engine': {
            'id': game.engine.id,
            'name': game.engine.name
        } if game.engine else None,
        'platforms': [{'id': p.id, 'name': p.name} for p in game.platforms.all()],
        'cover': game.cover.url if game.cover else None,
        'created_at': game.created_at.isoformat(),
        'updated_at': game.updated_at.isoformat(),
    } for game in games]
    
    return JsonResponse({'games': data, 'count': len(data)}, safe=False)


@api_key_required
def api_game_detail(request, pk):
    """API: Детали конкретной игры в формате JSON"""
    try:
        game = Game.objects.select_related('studio', 'engine').prefetch_related('platforms').get(pk=pk)
        
        data = {
            'id': game.id,
            'title': game.title,
            'release_year': game.release_year,
            'description': game.description,
            'studio': {
                'id': game.studio.id,
                'name': game.studio.name,
                'country': game.studio.country,
                'year_founded': game.studio.year_founded
            } if game.studio else None,
            'engine': {
                'id': game.engine.id,
                'name': game.engine.name
            } if game.engine else None,
            'platforms': [{'id': p.id, 'name': p.name} for p in game.platforms.all()],
            'cover': game.cover.url if game.cover else None,
            'created_at': game.created_at.isoformat(),
            'updated_at': game.updated_at.isoformat(),
        }
        
        return JsonResponse(data)
    except Game.DoesNotExist:
        return JsonResponse({'error': 'Game not found'}, status=404)


def api_demo(request):
    """Простая страница для проверки API-ключа из браузера."""
    return render(request, 'games/api_demo.html')

