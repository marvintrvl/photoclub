from django.urls import path
from .views import index
from . import views

urlpatterns = [
    path('', index, name='index'),
    path('impressum/', views.impressum, name='impressum'),
    path('kontakt/', views.kontakt, name='kontakt'),
    path('datenschutzerklaerung/', views.datenschutzerklaerung, name='datenschutzerklaerung'),
]