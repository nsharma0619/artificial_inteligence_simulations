from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='chatbot-home'),
    path('personal_details/', views.personal_details, name='chatbot-personal_details'),
    path('train/', views.train, name='chatbot-train'),
    path('<str:username>/chat/', views.chat, name='chatbot-chat'),
]