from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('game/<int:pk>/', views.game_detail, name='game_detail'),
    path('game/create/', views.game_create, name='game_create'),
    path('game/<int:pk>/update/', views.game_update, name='game_update'),
    path('game/<int:pk>/delete/', views.game_delete, name='game_delete'),
    
    # API endpoints
    path('api/games/', views.api_games_list, name='api_games_list'),
    path('api/games/<int:pk>/', views.api_game_detail, name='api_game_detail'),
]

