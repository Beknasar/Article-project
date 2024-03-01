from django.shortcuts import render, redirect
from .models import Article, STATUS_CHOICES
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from webapp.forms import ArticleForm


def index_view(request):
    is_admin = request.GET.get('is_admin', None)
    if is_admin:
        data = Article.objects.all()
    else:
        data = Article.objects.filter(status='moderated')
    return render(request, 'article/index.html', context={'articles': data})


def article_create_view(request):
    if request.method == "GET":
        return render(request, 'article/article_create.html', context={'form': ArticleForm()})
    elif request.method == 'POST':
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article = Article.objects.create(
                title=form.cleaned_data['title'],
                text=form.cleaned_data['text'],
                author=form.cleaned_data['author'],
                status=form.cleaned_data['status']
            )
            return redirect('webapp:article_view', pk=article.pk)
        else:
            return render(request, 'article/article_create.html', context={'form': form})
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


def article_update_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "GET":
        form = ArticleForm(initial={
            'title': article.title,
            'text': article.text,
            'author': article.author,
            'status': article.status
        })
        return render(request, 'article/article_update.html', context={
            'form': form,
            'article': article,
        })
    elif request.method == 'POST':
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article.title = form.cleaned_data['title']
            article.text = form.cleaned_data['text']
            article.author = form.cleaned_data['author']
            article.status = form.cleaned_data['status']
            article.save()
            return redirect('webapp:article_view', pk=article.pk)
        else:
            return render(request, 'article/article_update.html', context={
                'form': form,
                'article': article,
            })
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


def article_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'article/article_view.html', context={'article': article})


def article_delete_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "GET":
        return render(request, 'article/article_delete.html', context={"article": article})
    elif request.method == "POST":
        article.delete()
        return redirect('webapp:index')
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])
