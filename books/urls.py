from django.urls import path
from . import views

urlpatterns = [
    path('', views.books_index, name='books_index'),
    path('add/', views.book_create, name='book_create'),
    path('<int:pk>/', views.book_detail, name='book_detail'),
]
