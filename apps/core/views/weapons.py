from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
import uuid

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
            weapon.author = request.user if request.user.is_authenticated else None

            if not request.user.is_authenticated:
                weapon.anon_edit_token = uuid.uuid4()

            weapon.full_clean()
            weapon.save()

            if not request.user.is_authenticated and weapon.anon_edit_token:
                anon_tokens = request.session.get('anon_weapon_tokens', {})
                anon_tokens[str(weapon.id)] = str(weapon.anon_edit_token)
                request.session['anon_weapon_tokens'] = anon_tokens

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
        weapon_form = WeaponForm(instance=weapon)
        return render(request,
                      'core/weapon_details.html',
                      {'weapon_form': weapon_form,
                       'weapon': weapon}
                    )

    def post(self, request, pk):
        weapon = get_object_or_404(Weapon, pk=pk)

        is_user_owner = request.user.is_authenticated and weapon.author_id == request.user.id

        anon_tokens = request.session.get("anon_weapon_tokens", {})
        session_token = anon_tokens.get(str(weapon.id))
        is_anon_owner = (
                not request.user.is_authenticated
                and weapon.anon_edit_token is not None
                and session_token == str(weapon.anon_edit_token)
        )

        if not (is_user_owner or is_anon_owner):
            return (redirect('weapons'))

        weapon_form = weaponForm(request.POST, instance=weapon)
        if weapon_form.is_valid():
            weapon = weapon_form.save(commit=False)
            weapon.save()
            weapon_form.save_m2m()
            return redirect('weapon_details', pk=weapon.pk)
        return render(request,
                      'core/weapon_details.html',
                      {"weapon_form": weapon_form,
                       'weapon': weapon,
                       'errors': weapons_form.errors})