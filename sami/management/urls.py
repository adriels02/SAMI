from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.logar, name='logar'),

]