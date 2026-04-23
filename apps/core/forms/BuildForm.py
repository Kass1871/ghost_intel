from django import forms

from apps.core.models import Build

class BuildForm(forms.ModelForm):
    class Meta:
        model = Build
        exclude= (
            'author',
            'likes',
            'views',
            'datePublished',
            'dateUpdated'
        )