from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.db.models import Q
from django.views.generic import TemplateView, FormView, ListView
from webapp.forms import ArticleForm, SimpleSearchForm
from webapp.models import Article
from .base_views import FormView as CustomFormView


class IndexView(ListView):
    context_object_name = 'articles'
    template_name = 'article/index.html'
    paginate_by = 2
    paginate_orphans = 0

    def get_queryset(self):
        data = Article.objects.all()
        if not self.request.GET.get('is_admin', None):
            data = Article.objects.filter(status='moderated')

        # http://localhost:8000/?search=ygjkjhg
        form = SimpleSearchForm(data=self.request.GET)
        if form.is_valid():
            search = self.request.GET.get('search')
            if search:
                data = data.filter(Q(title__icontains=search) | Q(author__icontains=search))
        return data.order_by('-created_at')


class ArticleCreateView(CustomFormView):
    template_name = 'article/article_create.html'
    form_class = ArticleForm

    def form_valid(self, form):
        self.article = form.save()
        return super().form_valid(form)

    def get_redirect_url(self):
        return reverse('webapp:article_view', kwargs={'pk': self.article.pk})


class ArticleUpdateView(FormView):
    template_name = 'article/article_update.html'
    form_class = ArticleForm

    def dispatch(self, request, *args, **kwargs):
        self.article = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.pop('initial')
        kwargs['instance'] = self.article
        return kwargs

    def form_valid(self, form):
        self.article = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:article_view', kwargs={'pk': self.article.pk})

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Article, pk=pk)

    def get_context_data(self, **kwargs):
        # Получаем контекст от базового класса
        context = super().get_context_data(**kwargs)
        # Добавляем свои переменные контекста
        context['article'] = self.article
        return context


class ArticleView(TemplateView):
    template_name = 'article/article_view.html'
    paginate_comments_by = 2
    paginate_comments_orphans = 0

    def get_context_data(self, **kwargs):
        # Получаем контекст от базового класса
        context = super().get_context_data(**kwargs)
        # Добавляем свои переменные контекста
        pk = self.kwargs.get('pk')
        article = get_object_or_404(Article, pk=pk)
        comments, page, is_paginated = self.paginate_comments(article)

        context['article'] = article
        context['comments'] = comments
        context['page_obj'] = page
        context['is_paginated'] = is_paginated
        return context

    def paginate_comments(self, article):
        comments = article.comments.all().order_by('-created_at')
        if comments.count() > 0:
            paginator = Paginator(comments, self.paginate_comments_by, orphans=self.paginate_comments_orphans)
            page_number = self.request.GET.get('page', 1)
            page = paginator.get_page(page_number)

            is_paginated = paginator.num_pages > 1  # page.has_other_pages()
            return page.object_list, page, is_paginated
        else:
            return comments, None, False


def article_delete_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "GET":
        return render(request, 'article/article_delete.html', context={"article": article})
    elif request.method == "POST":
        article.delete()
        return redirect('webapp:index')
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])
