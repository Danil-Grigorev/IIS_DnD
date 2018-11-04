from django.contrib.auth.models import AnonymousUser

from .models import *


# Create your tests here.

def has_free_player(user):
    if isinstance(user, AnonymousUser):
        return False
    return not all([p.session_part for p in get_free_players(user.profile)])


def get_free_players(profile):
    p_list = Player.objects.filter(user=profile)
    session_leaders = Session.objects.filter(leader_id__in=p_list.values_list('id')).values_list('id')
    return p_list.exclude(id__in=session_leaders)  # Exclude session leaders
