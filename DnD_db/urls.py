from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.home, name='home'),
    path('new_session/', views.new_session, name='new_session'),
    path('new_character/', views.new_character, name='new_character'),
    path('new_player/', views.new_player, name='new_player')
]
