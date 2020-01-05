from django.urls import path, include
from django.contrib import admin

from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('dataproviders/', views.dataproviders, name='dataproviders'),
    path('docs/', views.docs, name='docs'),
    path('examples/', views.examples, name='examples'),
    path('getstarted/', views.getstarted, name='getstarted'),
]