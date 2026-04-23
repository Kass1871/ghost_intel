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
            weapons.author = request.user if request.user.is_authenticated else None

            if not request.user.is_authenticated:
                weapons.anon_edit_token = uuid.uuid4()

            weapons.full_clean()
            weapons.save()

            if not request.user.is_authenticated and weapons.anon_edit_token:
                anon_tokens = request.session.get('anon_weapons_tokens', {})
                anon_tokens[str(weapons.id)] = str(weapons.anon_edit_token)
                request.session['anon_weapons_tokens'] = anon_tokens

            weapons.tags.set(request.POST.getlist('tags'))
            weapons.relatedContent.set(request.POST.getlist('relatedContent'))
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
        weapons = get_object_or_404(weapons, pk=pk)

        is_user_owner = request.user.is_authenticated and weapons.author_id == request.user.id

        anon_tokens = request.session.get("anon_weapons_tokens", {})
        session_token = anon_tokens.get(str(weapons.id))
        is_anon_owner = (
                not request.user.is_authenticated
                and weapons.anon_edit_token is not None
                and session_token == str(weapons.anon_edit_token)
        )

        if not (is_user_owner or is_anon_owner):
            return (redirect('weapons'))

        weapons_form = weaponsForm(request.POST, instance=weapons)
        if weapons_form.is_valid():
            weapons = weapons_form.save(commit=False)
            weapons.save()
            weapons_form.save_m2m()
            return redirect('weapons_details', pk=weapons.pk)
        return render(request,
                      'core/weapons_details.html',
                      {"weapons_form": weapons_form,
                       'weapons': weapons,
                       'errors': weapons_form.errors})