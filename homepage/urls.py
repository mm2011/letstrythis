from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('donations/', views.donations, name='donations'),
    path('quiz/', views.quiz, name='quiz'),
    path('isCorrect/', views.isCorrect, name='isCorrect'),
    path('checkLogin/', views.checkLogin, name='checkLogin'),
    path('getScore/', views.getScore, name='getScore')
]