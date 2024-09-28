from django.urls import path
from funderr import views
from django.contrib import admin

urlpatterns = [
    path('', views.home, name='home'), # This is the home page. It will have a brief description of the app and a button to take the user to the form.
    ] 