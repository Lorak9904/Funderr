from django.urls import path
from . import views

urlpatterns = [
    path('check-key/', views.check_key, name='check_key'),
]