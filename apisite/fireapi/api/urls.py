from django.urls import path

from fireapi.api.views import ListFires

app_name = "fire_api"

urlpatterns = [
    path('', ListFires.as_view(), name='detail')
]