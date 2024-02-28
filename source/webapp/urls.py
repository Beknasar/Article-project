from django.urls import path
from .views import index_view, article_create_view, article_view

app_name = 'webapp'

urlpatterns = [
    path('', index_view, name='index'),
    path('article/<int:pk>/', article_view, name='article_view'),
    path('article/add/', article_create_view, name='article_create'),
]
