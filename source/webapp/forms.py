from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible
from .models import STATUS_CHOICES, Article, Tag


BROWSER_DATETIME_FORMAT = "%Y-%m-%dT%H:%M"
default_status = STATUS_CHOICES[0][0]


def at_least_10(string):
    if len(string) < 10:
        raise ValidationError('Заголовок слишком короткий!')


@deconstructible
class MinLengthValidator(BaseValidator):
    message = 'Value "%(value)s" has length of %(show_value)d! It should be at least %(limit_value)d symbols long!'
    code = 'too_short'

    def compare(self, value, limit):
        return value < limit

    def clean(self, value):
        return len(value)


class ArticleForm(forms.ModelForm):
    publish_at = forms.DateTimeField(required=False, label='Время публикации',
                                     input_formats=['%Y-%m-%d', BROWSER_DATETIME_FORMAT,
                                                    '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M',
                                                    '%Y-%m-%d %H:%M:%S'],
                                     widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Article
        fields = ['title', 'text', 'author', 'status', 'publish_at', 'tags']
        # widgets = {'publish_at': forms.DateTimeInput(attrs={'type': 'datetime-local'})}

    def clean(self):
        cleaned_data = super().clean()
        errors = []
        text = cleaned_data.get('text')
        title = cleaned_data.get('title')
        author = cleaned_data.get('author')
        if text and title and text == title:
            errors.append(ValidationError('Текст статьи не должен дублироваться в его заголовке!'))
        if title and author and title == author:
            errors.append(ValidationError('Вы не должны писать о себе! Это спам!'))
        if errors:
            raise ValidationError(errors)
        return cleaned_data


class CommentForm(forms.Form):
    article = forms.ModelChoiceField(queryset=Article.objects.all(), required=True, label='Статья')
