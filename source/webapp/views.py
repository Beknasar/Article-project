from django.shortcuts import render, redirect
from webapp.models import Article
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from webapp.forms import ArticleForm, BROWSER_DATETIME_FORMAT
from django.utils.timezone import make_naive
from django.views.generic import View, TemplateView


class IndexView(View):
    def get(self, request):
        is_admin = request.GET.get('is_admin', None)
        if is_admin:
            data = Article.objects.all()
        else:
            data = Article.objects.filter(status='moderated')
        return render(request, 'article/index.html', context={'articles': data})


class ArticleCreateView(View):
    def get(self, request):
        return render(request, 'article/article_create.html', context={'form': ArticleForm()})

    def post(self, request):
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            data = {}
            for key, value in form.cleaned_data.items():
                if value is not None:
                    data[key] = value
            article = Article.objects.create(**data)
            return redirect('webapp:article_view', pk=article.pk)
        else:
            return render(request, 'article/article_create.html', context={'form': form})


class ArticleUpdateView(TemplateView):
    template_name = 'article/article_update.html'

    def get_context_data(self, **kwargs):
        # Получаем контекст от базового класса
        context = super().get_context_data(**kwargs)
        # Добавляем свои переменные контекста
        pk = self.kwargs.get('pk')
        article = get_object_or_404(Article, pk=pk)

        initial = {}
        for key in 'title', 'text', 'author', 'status':
            initial[key] = getattr(article, key)
        initial['publish_at'] = make_naive(article.publish_at).strftime(BROWSER_DATETIME_FORMAT)
        form = ArticleForm(initial=initial)

        context['form'] = form
        context['article'] = article
        return context

    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            for key, value in form.cleaned_data.items():
                if value is not None:
                    setattr(article, key, value)
            article.save()
            return redirect('webapp:article_view', pk=article.pk)
        else:
            return self.render_to_response({
                'form': form,
                'article': article,
            })


class ArticleView(TemplateView):
    template_name = 'article/article_view.html'

    def get_context_data(self, **kwargs):
        # Получаем контекст от базового класса
        context = super().get_context_data(**kwargs)
        # Добавляем свои переменные контекста
        pk = self.kwargs.get('pk')
        article = get_object_or_404(Article, pk=pk)
        context['article'] = article
        return context


def article_delete_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "GET":
        return render(request, 'article/article_delete.html', context={"article": article})
    elif request.method == "POST":
        article.delete()
        return redirect('webapp:index')
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])
