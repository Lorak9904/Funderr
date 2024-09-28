from django.urls import path
from funderr import views
from django.contrib import admin

urlpatterns = [
    path('', views.home, name='home'), # This is the home page. It will have a brief description of the app and a button to take the user to the form.
    path('browse/', views.browse, name='browse') # This is the browse page. It will have a form that allows the user to search for NGOs and companies.
    ]