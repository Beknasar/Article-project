# Generated by Django 4.2.10 on 2024-03-07 08:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_tag_articletag_article_tags'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='tags',
            new_name='tags_old',
        ),
    ]
