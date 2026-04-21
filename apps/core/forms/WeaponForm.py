from django import forms

from apps.core.models import Weapon


class WeaponForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WeaponForm, self).__init__(*args, **kwargs)
        #self.helper.add_input(Submit())
    class Meta:
        model = Weapon
        fields = '__all__'
        #exclude = ('name',)
        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
        # }