from django.shortcuts import render
from .models import Article, STATUS_CHOICES
from django.http import HttpResponseRedirect, HttpResponseNotAllowed, Http404
from django.shortcuts import get_object_or_404


def index_view(request):
    is_admin = request.GET.get('is_admin', None)
    if is_admin:
        data = Article.objects.all()
    else:
        data = Article.objects.filter(status='moderated')
    return render(request, 'index.html', context={'articles': data})


def article_create_view(request):
    if request.method == "GET":
        return render(request, 'article_create.html', context={'status_choices': STATUS_CHOICES})
    elif request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')
        author = request.POST.get('author')
        status = request.POST.get('status')
        article = Article.objects.create(title=title, text=text, author=author, status=status)
        return HttpResponseRedirect(f'/article/{article.pk}/')
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


def article_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'article_view.html', context={'article': article})
