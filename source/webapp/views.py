from django.shortcuts import render
from .models import Article


def index_view(request):
    articles = Article.objects.all()
    context = {
        'articles': articles
    }
    return render(request, 'index.html', context)


def article_create_view(request):
    if request.method == "GET":
        return render(request, 'article_create.html')
    elif request.method == 'POST':
        context = {
            'title': request.POST.get('title'),
            'content': request.POST.get('content'),
            'author': request.POST.get('author')
        }
        return render(request, 'article_view.html', context)


def article_view(request):
    article_id = request.GET.get('pk')
    article = Article.objects.get(pk=article_id)
    context = {'article': article}
    return render(request, 'article_view.html', context)
