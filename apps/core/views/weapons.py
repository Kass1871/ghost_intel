from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views import View

from apps.core.forms.WeaponForm import WeaponForm
from apps.core.models import Weapon


def weapons_view(request):
    errors = {}
    data = {}
    if request.method == "POST":
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
                  {"weapon_types": Weapon.WEAPON_TYPES, "errors": errors, "data": data, 'weapon_list': weapon_list})

class weaponsDetails(View):
    def get(self, request, pk):
        weapon_form = WeaponForm()
        weapon = Weapon.objects.get(pk=pk)
        return render(request,
                      'core/weapon_details.html',
                      {'weapon_form': weapon_form}
                    )

    def post(self, request, pk):
        pass