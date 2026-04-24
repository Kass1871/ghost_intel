from django.contrib.auth import login
from django.shortcuts import redirect, render

from apps.core.forms.UserCreationForm import RegisterForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('welcome')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('welcome')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})