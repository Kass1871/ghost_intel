from django.shortcuts import render
from apps.core.models import Weapon


def weapons_view(request):
    if request.method == "POST":
        print(request.POST.get("weapons"))

    return render(request, 'core/weapons.html', {"weapon_types": Weapon.WEAPON_TYPES })