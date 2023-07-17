from django.contrib import admin
from django.urls import path,include 
from adminsignup import views
urlpatterns = [
    path('', views.index,name="index"),
    path('asignup', views.adminsignup,name="asignup"),
    path('alogin', views.adminlogin,name="alogin"),
    path('dashboard', views.admindashboard,name="dashboard"),
    path('addevent', views.addevent,name="addevent"),
    path('acalendar', views.acalendar,name="acalendar"),
    path('logout', views.logout,name=""),
    path('ueventcal', views.ueventcal,name="ueventcal"),
]
