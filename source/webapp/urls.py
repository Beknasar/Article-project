from django.urls import path
from .views import index_view, article_create_view, article_view

app_name = 'webapp'

urlpatterns = [
    path('', index_view),
    path('articles/add/', article_create_view),
    path('article/', article_view)
]
