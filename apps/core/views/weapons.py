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
            'thumbnail': request.FILES.get('thumbnail'),
            'name': request.POST.get('name'),
            'weapon_type': request.POST.get('weapon_type'),
            'weapon_rarity': request.POST.get('weapon_rarity') or 'unassigned',
            'description': request.POST.get('description'),
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
                   "weapon_rarities": Weapon.WEAPON_RARITIES,
                   "errors": errors,
                   "data": data,
                   'weapon_list': weapon_list})

class WeaponDetails(View):
    def get(self, request, pk):
        weapon = get_object_or_404(Weapon, pk=pk)
        weapon_form = WeaponForm(instance=weapon)

        can_edit = request.user.is_staff
        if not can_edit:
            for field in weapon_form.fields.values():
                field.disabled = True

        return render(request,
                          'core/weapon_details.html',
                          {'weapon_form': weapon_form,
                           'weapon': weapon,
                           'can_edit': can_edit}
                        )


    def post(self, request, pk):
        weapon = get_object_or_404(Weapon, pk=pk)

        if not request.user.is_staff:
            return redirect('weapon_details', pk=weapon.pk)

        if request.POST.get('delete'):
            weapon.delete()
            return redirect('weapons')

        weapon_form = WeaponForm(request.POST, request.FILES, instance=weapon)
        if weapon_form.is_valid():
            weapon = weapon_form.save()
            return redirect('weapon_details', pk=weapon.pk)
        return render(request,
                      'core/weapon_details.html',
                      {"weapon_form": weapon_form,
                       'weapon': weapon,
                       'errors': weapon_form.errors})