from django.urls import path
from . import views

urlpatterns = [
    path('', views.loadData, name='home'),
]