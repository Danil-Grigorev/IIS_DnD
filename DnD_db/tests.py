from django.contrib.auth.models import AnonymousUser

from .models import *


# Create your tests here.

def has_free_player(user):
    if isinstance(user, AnonymousUser):
        return False
    p_list = Player.objects.filter(user=user.profile)
    return any([not p.session_part for p in p_list])
