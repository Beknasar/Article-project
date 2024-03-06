from django.contrib import admin
from webapp.models import Article, Comment, Tag, ArticleTag


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'created_at']
    list_filter = ['author']
    search_fields = ['title', 'text']
    fields = ['title', 'author', 'text', 'status', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(ArticleTag)
