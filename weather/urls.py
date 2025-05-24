from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='weather'),
    path('city_not_found/<str:city_name>/', views.city_not_found, name='city_not_found'),
]