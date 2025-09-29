from django.urls import path
from . import views

urlpatterns =[
  path('', views.home, name='home'),
  path('user_profile/<str:pk>/', views.user_profile, name='user_profile'),
  path('register/' , views.register, name='register'),

  path('follow/<str:pk>/' , views.follow, name='follow'),
  path('approve_request/<str:pk>/' , views.approve_request, name='approve_request'),
]