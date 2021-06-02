from django.urls import path
from . import views

urlpatterns = [
    path('<slug:slug>/', views.stream_page, name='stream_page'),
    path('<slug:slug>/classwork/', views.classwork_page, name='classwork_page'),
    path('<slug:slug>/people/', views.people_page, name='people_page'),
]