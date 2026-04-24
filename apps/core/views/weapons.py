from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from apps.core.forms.WeaponForm import WeaponForm
from apps.core.models import Weapon


def weapons_view(request):
    errors = {}
    data = {}
    if request.method == "POST":
        if not request.user.is_staff:
            return redirect('weapons')
        data = {
            'name': request.POST.get('name'),
            'weapon_type': request.POST.get('weapon_type')
        }
        try:
            weapon = Weapon(**data)
            weapon.full_clean()
            weapon.save()

            return redirect('weapons')
        except ValidationError as e:
            errors = e.message_dict

    weapon_list = Weapon.objects.all()

    return render(request, 'core/weapons.html',
                  {"weapon_types": Weapon.WEAPON_TYPES,
                   "errors": errors,
                   "data": data,
                   'weapon_list': weapon_list})

class WeaponDetails(View):
    def get(self, request, pk):
        weapon = get_object_or_404(Weapon, pk=pk)
        if request.user.is_staff:
            weapon_form = WeaponForm(instance=weapon)
            return render(request,
                          'core/weapon_details.html',
                          {'weapon_form': weapon_form,
                           'weapon': weapon}
                        )
        return redirect('weapons')

    def post(self, request, pk):
        weapon = get_object_or_404(Weapon, pk=pk)

        if not request.user.is_staff:
            return (redirect('weapons'))

        weapon_form = WeaponForm(request.POST, instance=weapon)
        if weapon_form.is_valid():
            weapon = weapon_form.save(commit=False)
            weapon.save()
            weapon_form.save_m2m()
            return redirect('weapon_details', pk=weapon.pk)
        return render(request,
                      'core/weapon_details.html',
                      {"weapon_form": weapon_form,
                       'weapon': weapon,
                       'errors': weapon_form.errors})