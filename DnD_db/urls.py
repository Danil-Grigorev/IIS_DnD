from django.urls import path

from . import views
from .models import *

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.home, name='home'),

    path('change_role/player', views.role_change, {'role': 'Player'}, name='role_player'),
    path('change_role/author', views.role_change, {'role': 'Author'}, name='role_author'),
    path('change_role/session_leader', views.role_change, {'role': 'Session leader'}, name='role_session_leader'),

    path('take_session_part/<int:sess_id>/<int:player_id>/', views.participate_in_session, name='take_session_part'),
    path('send_invitation/<int:sess_id>/', views.send_invitation, name='send_invitation'),
    path('leave_session/<int:sess_id>/', views.leave_session, name='leave_session'),
    path('view_session/<int:sess_id>/', views.session_view, name='view_session'),
    # path('view_session/<int:sess_id>/kill/<int:ch_id>/', views.kill_character, name='kill_character'),
    path('view_session/<int:sess_id>/details/<int:ch_id>/', views.details_character, name='details_sess_character'),

    path('new_session/', views.new_session, name='new_session'),
    path('new_character/', views.new_character, name='new_character'),
    path('new_player/', views.new_player, name='new_player'),
    path('new_map/', views.new_map, name='new_map'),
    path('new_enemy/', views.new_enemy, name='new_enemy'),
    path('new_adventure/', views.new_adventure, name='new_adventure'),
    path('new_campaign/', views.new_campaign, name='new_campaign'),
    path('new_inventory/', views.new_inventory, name='new_inventory'),
    path('session_details/<int:sess_id>/send_invitation', views.send_invitation, name='send_invitation'),

    path('map_details/<int:id>/', views.details_map, name='detailed_map'),
    path('player_details/<int:id>/', views.details_player, name='detailed_player'),
    path('character_details/<int:id>/', views.details_character, name='detailed_character'),
    path('session_details/<int:id>/', views.details_session, name='detailed_session'),
    path('enemy_details/<int:id>/', views.details_enemy, name='detailed_enemy'),
    path('adventure_details/<int:id>/', views.details_adventure, name='detailed_adventure'),
    path('inventory_details/<int:id>/', views.details_inventory, name='detailed_inventory'),
    path('campaign_details/<int:id>/', views.details_campaign, name='detailed_campaign'),

    path('map_details/<int:id>/delete', views.delete, {'model': Map}, name='delete_map'),
    path('player_details/<int:id>/delete', views.delete, {'model': Player}, name='delete_player'),
    path('character_details/<int:id>/delete', views.delete, {'model': Character}, name='delete_character'),
    path('session_details/<int:id>/delete', views.delete, {'model': Session}, name='delete_session'),
    path('enemy_details/<int:id>/delete', views.delete, {'model': Enemy}, name='delete_enemy'),
    path('adventure_details/<int:id>/delete', views.delete, {'model': Adventure}, name='delete_adventure'),
    path('inventory_details/<int:id>/delete', views.delete, {'model': Inventory}, name='delete_inventory'),
    path('campaign_details/<int:id>/delete', views.delete, {'model': Campaign}, name='delete_campaign'),

    path('map_details/<int:id>/edit', views.edit_map, name='edit_map'),
    path('player_details/<int:id>/edit', views.edit_player, name='edit_player'),
    path('character_details/<int:id>/edit', views.edit_character, name='edit_character'),
    path('session_details/<int:id>/edit', views.edit_session, name='edit_session'),
    path('enemy_details/<int:id>/edit', views.edit_enemy, name='edit_enemy'),
    path('adventure_details/<int:id>/edit', views.edit_adventure, name='edit_adventure'),
    path('inventory_details/<int:id>/edit', views.edit_inventory, name='edit_inventory'),
    path('campaign_details/<int:id>/edit', views.edit_campaign, name='edit_campaign')
]
