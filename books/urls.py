from django.urls import path
from . import views

urlpatterns = [
    path('', views.books_index, name='books_index'),
    path('<int:pk>/', views.book_detail, name='book_detail'),
]
