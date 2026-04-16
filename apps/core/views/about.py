from django.http import HttpResponse
from django.shortcuts import render


def about_view(request):
    return render(request, 'about-project.html')