from django.urls import path
from . import views

urlpatterns = [
    path('', views.queryDataBase, name='home'),
    path('upload_excel/', views.upload_excel, name='uploadExcel'),
    path('delete_data/', views.delete_data, name='deleteData'),
    path('confirm_delete/', views.confirm_delete, name='confirmDelete'),

]