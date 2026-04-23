from django.urls import path
from apps.core import views
from apps.core.views.weapons import WeaponDetails
from apps.core.views.builds import BuildDetails
from apps.core.views.news import  NewsDetails

urlpatterns = [
    path('about/', views.about, name='about_project'),
    path('', views.welcome, name='welcome'),
    path("weapons/", views.weapons, name="weapons"),
    #path('weapons/<int:pk>/delete/', views.weapons.delete_weapon, name="delete_weapon"),
    path("weapons/<int:pk>/", WeaponDetails.as_view(), name="weapon_details"),
    path("builds/", views.builds, name="builds"),
    path("builds/<int:pk>/", BuildDetails.as_view(), name="build_details"),
    path("news/", views.news, name="news"),
    path("news/<int:pk>/", NewsDetails.as_view(), name="news_details")
]