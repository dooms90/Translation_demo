from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('app/', views.translator_app, name='translator_app'),
    path('api/translate/', views.translate, name='translate'),
]