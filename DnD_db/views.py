from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

from .forms import *
from .tests import *


def home(request):
    if request.user.is_anonymous:
        return render(request, 'home_pages/player_home.html', {})

    context = {
        'has_player': has_free_player(request.user),
        'players': Player.objects.filter(user=request.user.profile),
    }
    if request.user.profile.role == "Author":
        context['campaigns'] = Campaign.objects.filter(author=request.user.profile)
        context['characters'] = Character.objects.filter(author__user=request.user.profile)
        context['adventures'] = Adventure.objects.filter(author=request.user.profile)
        context['enemies'] = Enemy.objects.filter(author=request.user.profile)
        context['maps'] = Map.objects.filter(author=request.user.profile)
        context['items'] = Inventory.objects.filter(author=request.user.profile)

        return render(request, 'home_pages/author_home.html', context)
    elif request.user.profile.role == "Session leader":
        leaders = Player.objects.filter(user=request.user.profile)
        context['leaded_sessions'] = Session.objects.filter(author__in=leaders)
        context['campaigns'] = Campaign.objects.exists()
        return render(request, 'home_pages/session_leader_home.html', context)
    elif request.user.profile.role == "Player":
        pl_part_sess = Player.objects.filter(user=request.user.profile).values_list('session_part')
        part_sessions_l = Session.objects.filter(id__in=pl_part_sess)
        context['participated_sessions'] = part_sessions_l
        context['invited_sessions'] = Session.objects.exclude(id__in=part_sessions_l.values_list('id'))

        return render(request, 'home_pages/player_home.html', context)
    else:
        return HttpResponseNotFound('<h1>Unknown role detected</h1>')


@login_required(login_url='/login/')
def role_change(request, role):
    user = get_object_or_404(User, id=request.user.id)
    user.profile.role = role
    user.profile.save()
    return redirect('home')


@login_required(login_url='/login/')
def participate_in_session(request, sess_id):
    if request.method == 'POST':
        form = TakePartS(request.user.profile, sess_id, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully joined session.')
            return redirect(Session.objects.get(id=form.sess_id).get_participator_url())
        else:
            messages.error(request, "Can't take part in session, invalid form detected")
    else:
        form = TakePartS(request.user.profile, sess_id)
    context = {
        'title': 'Session participation',
        'form': form,
        'name': 'Choose session and player',
        'submit_name': 'Start'
    }
    return render(request, 'forms/form_base.html', context)


@login_required(login_url='/login/')
def session_view(request, sess_id):
    sess = get_object_or_404(Session, id=sess_id)
    if request.method == 'POST':
        form = CreateMessage(request.user.profile, sess, request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CreateMessage(request.user.profile, sess, request.POST)
    context = {
        'participator_chat': Message.objects.filter(session=sess),
        'form': form,
        'viewer': Player.objects.filter(user=request.user.profile).filter(session_part=sess)[0],
    }
    return render(request, 'in_session_view.html', context)


@login_required(login_url='/login')
def details_campaign(request, id):
    obj = get_object_or_404(Campaign, id=id)
    return render(request, 'detailed_views/details_campaign.html', {'obj_details': obj})


@login_required(login_url='/login')
def details_map(request, id):
    obj = get_object_or_404(Map, id=id)
    return render(request, 'detailed_views/details_map.html', {'obj_details': obj})


@login_required(login_url='/login')
def details_player(request, id):
    obj = get_object_or_404(Player, id=id)
    return render(request, 'detailed_views/details_player.html', {'obj_details': obj})


@login_required(login_url='/login')
def details_character(request, id):
    obj = get_object_or_404(Character, id=id)
    return render(request, 'detailed_views/details_character.html', {'obj_details': obj})


@login_required(login_url='/login')
def details_session(request, id):
    sess = get_object_or_404(Session, id=id)
    try:
        participated_player = Player.objects.filter(session_part=sess).get(user=request.user.profile)
    except ObjectDoesNotExist:
        participated_player = None

    is_author = sess.author.user == request.user.profile

    context = {
        'participator': participated_player,
        'is_creator': is_author,
        'obj_details': sess,
    }
    return render(request, 'detailed_views/details_session.html', context)


@login_required(login_url='/login')
def details_enemy(request, id):
    obj = get_object_or_404(Enemy, id=id)
    return render(request, 'detailed_views/details_enemy.html', {'obj_details': obj})


@login_required(login_url='/login')
def details_adventure(request, id):
    obj = get_object_or_404(Adventure, id=id)
    return render(request, 'detailed_views/details_adventure.html', {'obj_details': obj})


@login_required(login_url='/login')
def details_inventory(request, id):
    obj = get_object_or_404(Inventory, id=id)
    return render(request, 'detailed_views/details_inventory.html', {'obj_details': obj})


@login_required(login_url='/home/')
@can_delete_object
def delete(request, id, model):
    obj = get_object_or_404(model, id=id)
    if request.method == 'POST':
        name = str(obj)
        obj.delete()
        messages.success(request, '{} was deleted.'.format(name))
        return redirect('home')
    return render(request, 'confirm_action.html', {'obj_details': obj, 'operation': 'delete'})


@login_required(login_url='/home/')
def leave_session(request, sess_id):
    session = Session.objects.get(id=sess_id)
    if request.method == 'POST':
        player = Player.objects.filter(user=request.user.profile).get(session_part=session)
        player.session_part = None
        player.save()
        return redirect('home')
    else:
        return render(request, 'confirm_action.html', {'obj_details': session, 'operation': 'leave'})


@login_required(login_url='/home/')
def edit_player(request, id):
    obj = get_object_or_404(Player, id=id)
    if request.method == 'POST':
        form = CreatePlayer(request.user.profile, request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "'{}' was updated successfully.".format(obj))
            return redirect('home')
        else:
            messages.error(request, "Can't update '{}', invalid form detected".format(obj))
    else:
        form = CreatePlayer(request.user.profile, instance=obj)

    context = {
        'title': 'Edit player',
        'form': form,
        'name': 'Edit player',
        'submit_name': 'Submit changes'
    }
    return render(request, 'forms/form_base.html', context)


@login_required(login_url='/home/')
def edit_session(request, id):
    obj = get_object_or_404(Session, id=id)
    if request.method == 'POST':
        form = CreateSession(request.user.profile, request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "'{}' was updated successfully.".format(obj))
            return redirect('home')
        else:
            messages.error(request, "Can't update '{}', invalid form detected".format(obj))
    else:
        form = CreateSession(request.user.profile, instance=obj)

    context = {
        'title': 'Edit session',
        'form': form,
        'name': 'Edit session',
        'submit_name': 'Submit changes'
    }
    return render(request, 'forms/form_base.html', context)


@login_required(login_url='/home/')
def edit_character(request, id):
    obj = get_object_or_404(Character, id=id)
    if request.method == 'POST':
        form = CreateCharacter(request.user.profile, request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "'{}' was updated successfully.".format(obj))
            return redirect('home')
        else:
            messages.error(request, "Can't update '{}', invalid form detected".format(obj))
    else:
        form = CreateCharacter(request.user.profile, instance=obj)

    context = {
        'title': 'Edit character',
        'form': form,
        'name': 'Edit character',
        'submit_name': 'Submit changes'
    }
    return render(request, 'forms/form_base.html', context)


@login_required(login_url='/home/')
def edit_enemy(request, id):
    obj = get_object_or_404(Enemy, id=id)
    if request.method == 'POST':
        form = CreateEnemy(request.user.profile, request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "'{}' was updated successfully.".format(obj))
            return redirect('home')
        else:
            messages.error(request, "Can't update '{}', invalid form detected".format(obj))
    else:
        form = CreateEnemy(request.user.profile, instance=obj)

    context = {
        'title': 'Edit enemy',
        'form': form,
        'name': 'Edit enemy',
        'submit_name': 'Submit changes'
    }
    return render(request, 'forms/form_base.html', context)


@login_required(login_url='/home/')
def edit_adventure(request, id):
    obj = get_object_or_404(Adventure, id=id)
    if request.method == 'POST':
        form = CreateAdventure(request.user.profile, request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "'{}' was updated successfully.".format(obj))
            return redirect('home')
        else:
            messages.error(request, "Can't update '{}', invalid form detected".format(obj))
    else:
        form = CreateAdventure(request.user.profile, instance=obj)

    context = {
        'title': 'Edit adventure',
        'form': form,
        'name': 'Edit adventure',
        'submit_name': 'Submit changes'
    }
    return render(request, 'forms/form_base.html', context)


@login_required(login_url='/home/')
def edit_campaign(request, id):
    obj = get_object_or_404(Campaign, id=id)
    if request.method == 'POST':
        form = CreateCampaign(request.user.profile, request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "'{}' was updated successfully.".format(obj))
            return redirect('home')
        else:
            messages.error(request, "Can't update '{}', invalid form detected".format(obj))
    else:
        form = CreateCampaign(request.user.profile, instance=obj)

    context = {
        'title': 'Edit campaign',
        'form': form,
        'name': 'Edit campaign',
        'submit_name': 'Submit changes'
    }
    return render(request, 'forms/form_base.html', context)


@login_required(login_url='/home/')
def edit_inventory(request, id):
    obj = get_object_or_404(Inventory, id=id)
    if request.method == 'POST':
        form = CreateInventory(request.user.profile, request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "'{}' was updated successfully.".format(obj))
            return redirect('home')
        else:
            messages.error(request, "Can't update '{}', invalid form detected".format(obj))
    else:
        form = CreateInventory(request.user.profile, instance=obj)

    context = {
        'title': 'Edit inventory',
        'form': form,
        'name': 'Edit inventry',
        'submit_name': 'Submit changes'
    }
    return render(request, 'forms/form_base.html', context)


@login_required(login_url='/home/')
def edit_map(request, id):
    obj = get_object_or_404(Map, id=id)
    if request.method == 'POST':
        form = CreateMap(request.user.profile, request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "'{}' was updated successfully.".format(obj))
            return redirect('home')
        else:
            messages.error(request, "Can't update '{}', invalid form detected".format(obj))
    else:
        form = CreateMap(request.user.profile, instance=obj)

    context = {
        'title': 'Edit map',
        'form': form,
        'name': 'Edit map',
        'submit_name': 'Submit changes'
    }
    return render(request, 'forms/form_base.html', context)


@login_required(login_url='/login/')
def new_enemy(request):
    if request.method == 'POST':
        form = CreateEnemy(request.user.profile, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Enemy was created successfully.')
            return redirect('home')
        else:
            messages.error(request, "Can't create enemy, invalid form detected")
    else:
        form = CreateEnemy(request.user.profile)

    context = {
        'title': 'Create enemy',
        'form': form,
        'name': 'New enemy',
        'submit_name': 'Add enemy'
    }
    return render(request, 'forms/form_base.html', context)


@login_required(login_url='/login/')
def new_adventure(request):
    if request.method == 'POST':
        form = CreateAdventure(request.user.profile, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Adventure was created successfully.')
            return redirect('home')
        else:
            messages.error(request, "Can't create adventure, invalid form detected")
    else:
        form = CreateAdventure(request.user.profile)

    context = {
        'title': 'Create adventure',
        'form': form,
        'name': 'New adventure',
        'submit_name': 'Add adventure'
    }
    return render(request, 'forms/form_base.html', context)


@login_required(login_url='/login/')
def new_campaign(request):
    if request.method == 'POST':
        form = CreateCampaign(request.user.profile, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Campaign was created successfully.')
            return redirect('home')
        else:
            messages.error(request, "Can't create campaign, invalid form detected")
    else:
        form = CreateCampaign(request.user.profile)

    context = {
        'title': 'Create campaign',
        'form': form,
        'name': 'New campaign',
        'submit_name': 'Add campaign'
    }
    return render(request, 'forms/form_base.html', context)


@login_required(login_url='/login/')
def new_inventory(request):
    if request.method == 'POST':
        form = CreateInventory(request.user.profile, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item was created successfully.')
            return redirect('home')
        else:
            messages.error(request, "Can't create item, invalid form detected")
    else:
        form = CreateInventory(request.user.profile)

    context = {
        'title': 'Create item',
        'form': form,
        'name': 'New item',
        'submit_name': 'Add item'
    }
    return render(request, 'forms/form_base.html', context)


@login_required(login_url='/login/')
def new_session(request):
    if request.method == 'POST':
        form = CreateSession(request.user.profile, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Session was created successfully.')
            return redirect('home')
        else:
            messages.error(request, "Can't create session, invalid form detected")
    else:
        form = CreateSession(request.user.profile)
    context = {
        'title': 'Create session',
        'form': form,
        'name': 'New session',
        'submit_name': 'Create session'
    }
    return render(request, 'forms/form_base.html', context)


# @user_passes_test(has_free_player, login_url='/home/')
@login_required(login_url='/login/')
def new_character(request):
    if request.method == 'POST':
        form = CreateCharacter(request.user.profile, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Character was created successfully.')
            return redirect('home')
        else:
            messages.error(request, "Can't create character, invalid form detected")
    else:
        form = CreateCharacter(request.user.profile)

    context = {
        'title': 'Create character',
        'form': form,
        'name': 'New character',
        'submit_name': 'Add character'
    }

    return render(request, 'forms/form_base.html', context)


@login_required(login_url='/login/')
def new_player(request):
    if request.method == 'POST':
        form = CreatePlayer(request.user.profile, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Player was created successfully.')
            return redirect('home')
        else:
            messages.error(request, "Can't create player, invalid form detected")
    else:
        form = CreatePlayer(request.user.profile)

    context = {
        'title': 'Create player',
        'form': form,
        'name': 'New player',
        'submit_name': 'Add player'
    }

    return render(request, 'forms/form_base.html', context)


@login_required(login_url='/login/')
def new_map(request):
    if request.method == 'POST':
        form = CreateMap(request.user.profile, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Map was created successfully.')
            return redirect('home')
        else:
            messages.error(request, "Can't create map, invalid form detected")
    else:
        form = CreateMap(request.user.profile)

    context = {
        'title': 'Create map',
        'form': form,
        'name': 'New map',
        'submit_name': 'Add map'
    }
    return render(request, 'forms/form_base.html', context)
