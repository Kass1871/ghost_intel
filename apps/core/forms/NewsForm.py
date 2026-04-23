from django import forms

from apps.core.models import News

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        exclude = (
            'author',
            'datePublished',
            'dateUpdated'
        )