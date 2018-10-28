from django.urls import path

from . import views
from .models import *

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.home, name='home'),
    path('new_session/', views.new_session, name='new_session'),
    path('new_character/', views.new_character, name='new_character'),
    path('new_player/', views.new_player, name='new_player'),
    path('new_map/', views.new_map, name='new_map'),
    path('new_enemy/', views.new_enemy, name='new_enemy'),
    path('new_adventure/', views.new_adventure, name='new_adventure'),
    path('new_campaign/', views.new_campaign, name='new_campaign'),

    path('map_details/<int:id>/', views.details_map, {'model': Map}, name='detailed_map'),
    path('player_details/<int:id>/', views.details_player, {'model': Player}, name='detailed_player'),
    path('character_details/<int:id>/', views.details_character, {'model': Character}, name='detailed_character'),
    path('session_details/<int:id>/', views.details_session, {'model': Session}, name='detailed_session'),
    path('enemy_details/<int:id>/', views.details_enemy, {'model': Enemy}, name='detailed_enemy'),
    path('adventure_details/<int:id/>', views.details_adventure, {'model': Adventure}, name='detailed_adventure'),

    path('map_details/<int:id>/delete', views.delete, {'model': Map}, name='delete_map'),
    path('player_details/<int:id>/delete', views.delete, {'model': Player}, name='delete_player'),
    path('character_details/<int:id>/delete', views.delete, {'model': Character}, name='delete_character'),
    path('session_details/<int:id>/delete', views.delete, {'model': Session}, name='delete_session'),
    path('enemy_details/<int:id/delete>', views.delete, {'model': Enemy}, name='delete_enemy'),
    path('adventure_details/<int:id/delete>', views.delete, {'model': Adventure}, name='delete_adventure'),
]
