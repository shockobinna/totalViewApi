from django.urls import path
from . import views

urlpatterns = [
    path('', views.queryDataBase, name='home'),
    path('upload_excel/', views.upload_excel, name='uploadExcel'),
]