from django.urls import path
from . import views

app_name = 'maintenance'

urlpatterns = [
    path(route='',view=views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('upload/', views.upload_document, name='upload_document'),
    path('list/', views.list_documents, name='list_documents'),
    path('q_and_a/', views.q_and_a, name='q_and_a'),
]