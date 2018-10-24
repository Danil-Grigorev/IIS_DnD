from .models import *
# Create your tests here.

def has_free_player(user):
    try:
        p_list = Player.objects.get(user=user)
    except Player.DoesNotExist:
        return False
    else:
        return not p_list.session_part.exists()
