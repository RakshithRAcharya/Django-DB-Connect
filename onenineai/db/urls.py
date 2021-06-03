from django.urls import path
from db import views

urlpatterns = [
    path('table_data/', views.show, name='show'),
    path('connection/', views.login, name='connect'),
    path('db/', views.get_DB_details, name='getDB'),
    path('', views.home, name='home'),
    path('app_data/', views.app_data, name='app-data'),
]