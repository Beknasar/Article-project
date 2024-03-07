from django.db import migrations


def transfer_tags(apps, schema_editor):
    Article = apps.get_model('webapp.Article')
    for article in Article.objects.all():
        article.tags.set(article.tags_old.all())


def rollback_transfer(apps, schema_editor):
    Article = apps.get_model('webapp.Article')
    for article in Article.objects.all():
        article.tags_old.set(article.tags.all())


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_article_tags_alter_article_tags_old'),
    ]

    operations = [
        migrations.RunPython(transfer_tags, rollback_transfer)
    ]
