from django.contrib.auth.models import AnonymousUser

from .models import *


# Create your tests here.

def has_free_player(user):
    if isinstance(user, AnonymousUser):
        return False
    p_list = Player.objects.filter(user=user.profile)
    session_leaders = Session.objects.filter(leader_id__in=p_list.values_list('id')).values_list('id')
    p_list = p_list.exclude(id__in=session_leaders)  # Exclude session leaders
    return not all([p.session_part for p in p_list])
