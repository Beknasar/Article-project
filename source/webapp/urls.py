from django.urls import path
from .views import IndexView, ArticleCreateView, ArticleView, ArticleUpdateView, article_delete_view

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('article/add/', ArticleCreateView.as_view(), name='article_create'),
    path('article/<int:pk>/', ArticleView.as_view(), name='article_view'),
    path('article/<int:pk>/update/', ArticleUpdateView.as_view(), name="article_update"),
    path('article/<int:pk>/delete/', article_delete_view, name='article_delete'),
]
