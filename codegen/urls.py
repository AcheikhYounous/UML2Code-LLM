# codegen/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.generate_view, name='generate'),
]
