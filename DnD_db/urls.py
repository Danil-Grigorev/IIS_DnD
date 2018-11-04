from django.urls import path

from . import views
from .models import *

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.home, name='home'),

    path('change_role/player', views.role_change, {'role': 'Player'}, name='role_player'),
    path('change_role/author', views.role_change, {'role': 'Author'}, name='role_author'),
    path('change_role/session_leader', views.role_change, {'role': 'Session leader'}, name='role_session_leader'),

    path('new_session/', views.new_session, name='new_session'),
    path('new_character/', views.new_character, name='new_character'),
    path('new_player/', views.new_player, name='new_player'),
    path('new_map/', views.new_map, name='new_map'),
    path('new_enemy/', views.new_enemy, name='new_enemy'),
    path('new_adventure/', views.new_adventure, name='new_adventure'),
    path('new_campaign/', views.new_campaign, name='new_campaign'),
    path('new_inventory/', views.new_inventory, name='new_inventory'),

    path('map_details/<int:id>/', views.details_map, {'model': Map}, name='detailed_map'),
    path('player_details/<int:id>/', views.details_player, {'model': Player}, name='detailed_player'),
    path('character_details/<int:id>/', views.details_character, {'model': Character}, name='detailed_character'),
    path('session_details/<int:id>/', views.details_session, {'model': Session}, name='detailed_session'),
    path('enemy_details/<int:id>/', views.details_enemy, {'model': Enemy}, name='detailed_enemy'),
    path('adventure_details/<int:id>/', views.details_adventure, {'model': Adventure}, name='detailed_adventure'),
    path('inventory_details/<int:id>/', views.details_inventory, {'model': Inventory}, name='detailed_inventory'),
    path('campaign_details/<int:id>/', views.details_campaign, {'model': Campaign}, name='detailed_campaign'),

    path('map_details/<int:id>/delete', views.delete, {'model': Map}, name='delete_map'),
    path('player_details/<int:id>/delete', views.delete, {'model': Player}, name='delete_player'),
    path('character_details/<int:id>/delete', views.delete, {'model': Character}, name='delete_character'),
    path('session_details/<int:id>/delete', views.delete, {'model': Session}, name='delete_session'),
    path('enemy_details/<int:id>/delete', views.delete, {'model': Enemy}, name='delete_enemy'),
    path('adventure_details/<int:id>/delete', views.delete, {'model': Adventure}, name='delete_adventure'),
    path('inventory_details/<int:id>/delete', views.delete, {'model': Inventory}, name='delete_inventory'),
    path('campaign_details/<int:id>/delete', views.delete, {'model': Campaign}, name='delete_campaign'),

    path('map_details/<int:id>/edit', views.edit, {'model': Map}, name='edit_map'),
    path('player_details/<int:id>/edit', views.edit, {'model': Player}, name='edit_player'),
    path('character_details/<int:id>/edit', views.edit, {'model': Character}, name='edit_character'),
    path('session_details/<int:id>/edit', views.edit, {'model': Session}, name='edit_session'),
    path('enemy_details/<int:id>/edit', views.edit, {'model': Enemy}, name='edit_enemy'),
    path('adventure_details/<int:id>/edit', views.edit, {'model': Adventure}, name='edit_adventure'),
    path('inventory_details/<int:id>/edit', views.edit, {'model': Inventory}, name='edit_inventory'),
    path('campaign_details/<int:id>/edit', views.edit, {'model': Campaign}, name='edit_campaign')
]
