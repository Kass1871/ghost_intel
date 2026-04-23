from django import forms

from apps.core.models import Weapon


class WeaponForm(forms.ModelForm):
    class Meta:
        model = Weapon
        fields = '__all__'