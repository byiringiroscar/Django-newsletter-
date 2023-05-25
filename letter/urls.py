from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('mail_letter/', views.mail_letter, name='mail_letter')
]