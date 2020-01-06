from django.urls import path, include
from django.contrib import admin

from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('dataproviders/', views.dataproviders, name='dataproviders'),
    path('docs/', views.docs, name='docs'),
    path('examples/', views.examples, name='examples'),
    path('getstarted/', views.getstarted, name='getstarted'),
    path('accounts/profile/', views.profile, name='profile'),
    # path('accounts/delete_account/(?P<username>[\w|\W.-]+)/$', views.delete_user, name='delete_account')
]