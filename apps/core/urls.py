from django.urls import path
from apps.core import views

urlpatterns = [
    path('about/', views.about, name='about_project'),
    path('', views.welcome, name='welcome'),
    path("weapons/", views.weapons, name="weapons"),
    path("weapons/<int:pk>/", views.weapons, name="weapon_details")
]