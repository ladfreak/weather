from django.contrib import admin
from django.urls import path
from forecast import views

urlpatterns = [
    path('', views.home,name="home"),
    path('city_remove/<str:cname>',views.city_remove,name="city_remove"),
]