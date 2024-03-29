# Generated by Django 4.2.10 on 2024-03-07 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_rename_tags_article_tags_old'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='articles', to='webapp.tag', verbose_name='Теги'),
        ),
        migrations.AlterField(
            model_name='article',
            name='tags_old',
            field=models.ManyToManyField(blank=True, related_name='article_set', through='webapp.ArticleTag', to='webapp.tag', verbose_name='Теги'),
        ),
    ]
