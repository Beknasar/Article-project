from django.shortcuts import render
from .models import Article
from django.http import HttpResponseRedirect


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
        title = request.POST.get('title')
        text = request.POST.get('text')
        author = request.POST.get('author')
        article = Article.objects.create(title=title, text=text, author=author)
        return HttpResponseRedirect(f'/article?article_id={article.pk}')


def article_view(request):
    article_id = request.GET.get('pk')
    article = Article.objects.get(pk=article_id)
    return HttpResponseRedirect(f'/article?article_id={article.pk}')
