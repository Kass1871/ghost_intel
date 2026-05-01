import uuid
import json

from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from apps.core.forms.BuildForm import BuildForm
from apps.core.models import Build


def builds_view(request):
    errors = {}
    data = {}

    if request.method == "POST":
        data = {
            'title': request.POST.get('title'),
            'slug': request.POST.get('slug'),
            'description': request.POST.get('description'),
            'content': request.POST.get('content'),
            'build_class': request.POST.get('build_class'),
            'subclass': request.POST.get('subclass'),
            'build_type': request.POST.get('build_type'),
            'difficulty': request.POST.get('difficulty'),
            'statsPriority': request.POST.get('statsPriority'),
            'expansion': request.POST.get('expansion')
        }
        armor_mods = {
            "helmet": [m.strip() for m in request.POST.get("armor_helmet", "").split(",") if m.strip()],
            "arms": [m.strip() for m in request.POST.get("armor_arms", "").split(",") if m.strip()],
            "chest": [m.strip() for m in request.POST.get("armor_chest", "").split(",") if m.strip()],
            "legs": [m.strip() for m in request.POST.get("armor_legs", "").split(",") if m.strip()],
            "class_item": [m.strip() for m in request.POST.get("armor_class_item", "").split(",") if m.strip()],
        }
        armor_mods = {slot: mods for slot, mods in armor_mods.items() if mods}
        data["armorMods"] = armor_mods if armor_mods else {}

        try:
            build = Build(**data)
            build.author = request.user if request.user.is_authenticated else None

            if not request.user.is_authenticated:
                build.anonymous = build.anon_edit_token = uuid.uuid4()

            build.full_clean()
            build.save()

            if not request.user.is_authenticated and build.anon_edit_token:
                anon_tokens = request.session.get('anon_build_tokens', {})
                anon_tokens[str(build.id)] = str(build.anon_edit_token)
                request.session['anon_build_tokens'] = anon_tokens

            build.tags.set(request.POST.getlist('tags'))
            build.exotics.set(request.POST.getlist('exotics'))
            build.weapons.set(request.POST.getlist('weapons'))

            return redirect('builds')
        except ValidationError as e:
            errors = e.message_dict

    build_list = Build.objects.all()

    return render(request, 'core/builds.html',
                  {"build_class": Build.CLASSES,
                   "subclass": Build.SUBCLASSES,
                   "build_type": Build.BUILD_TYPES,
                   "difficulty": Build.DIFFICULTY_CHOICES,
                   "errors": errors,
                   "data": data,
                   'build_list': build_list})

class BuildDetails(View):
    def get(self, request, pk):
        build = get_object_or_404(Build, pk=pk)
        build_form = BuildForm(instance=build)

        is_user_owner = request.user.is_authenticated and build.author_id == request.user.id
        is_anon_owner = (
                not request.user.is_authenticated
                and build.anon_edit_token is not None
                and session_token == str(build.anon_edit_token)
        )

        can_edit = request.user.is_staff or is_user_owner or is_anon_owner
        if not can_edit:
            for field in build_form.fields.values():
                field.disabled = True

        return render(request,
                      'core/build_details.html',
                      {'build_form': build_form,
                       'build': build,
                       'can_edit': can_edit}
                    )

    def post(self, request, pk):
        build = get_object_or_404(Build, pk=pk)

        is_user_owner = request.user.is_authenticated and build.author_id == request.user.id

        post_data = request.POST.copy()
        post_data.setdefault("slug", build.slug)

        required_fields = ['build_class', 'subclass', 'build_type', 'difficulty']
        for field in required_fields:
            if field not in post_data:
                post_data[field] = getattr(build, field)

        anon_tokens = request.session.get("anon_build_tokens", {})
        session_token = anon_tokens.get(str(build.id))
        is_anon_owner = (
                not request.user.is_authenticated
                and build.anon_edit_token is not None
                and session_token == str(build.anon_edit_token)
        )
        can_edit = request.user.is_staff or is_user_owner or is_anon_owner

        if not (is_user_owner or is_anon_owner or can_edit):
            return(redirect('builds'))

        if request.POST.get('delete'):
            build.delete()
            return redirect('builds')

        build_form = BuildForm(post_data, instance=build)
        armor_mods = {
            "helmet": [m.strip() for m in request.POST.get("armor_helmet", "").split(",") if m.strip()],
            "arms": [m.strip() for m in request.POST.get("armor_arms", "").split(",") if m.strip()],
            "chest": [m.strip() for m in request.POST.get("armor_chest", "").split(",") if m.strip()],
            "legs": [m.strip() for m in request.POST.get("armor_legs", "").split(",") if m.strip()],
            "class_item": [m.strip() for m in request.POST.get("armor_class_item", "").split(",") if m.strip()],
        }
        armor_mods = {slot: mods for slot, mods in armor_mods.items() if mods}

        if build_form.is_valid():
            build = build_form.save(commit=False)
            build.armorMods = armor_mods if armor_mods else {}
            build.save()
            build_form.save_m2m()
            return redirect('build_details', pk=build.pk)
        return render(request,
                      'core/build_details.html',
                      {"build_form": build_form,
                       'build': build,
                       'errors': build_form.errors,
                       'can_edit': can_edit,
                       'is_user_owner': is_user_owner})