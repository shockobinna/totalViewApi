from django.urls import path
from . import views

urlpatterns = [
    path('loadFile/', views.loadData, name='loadData'),
]