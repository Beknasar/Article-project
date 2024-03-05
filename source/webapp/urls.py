from django.urls import path
from .views import IndexView, article_create_view, article_view, article_update_view, article_delete_view

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('article/add/', article_create_view, name='article_create'),
    path('article/<int:pk>/', article_view, name='article_view'),
    path('article/<int:pk>/update/', article_update_view, name="article_update"),
    path('article/<int:pk>/delete/', article_delete_view, name='article_delete'),
]
