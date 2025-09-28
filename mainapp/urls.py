from django.urls import path
from . import views

urlpatterns =[
  path('', views.home, name='home'),
  path('chatroom/<str:pk>/', views.chatroom, name='chatroom'),
  path('register/', views.register, name='register'),
]