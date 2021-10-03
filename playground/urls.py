from django.urls import path
from . import views

urlpatterns = [
    path('sabrina/', views.love_sabrina),
    path('say_hello2', views.say_hello2)
]
