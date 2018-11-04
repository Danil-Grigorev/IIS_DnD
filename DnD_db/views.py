from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import *
from .tests import *

model_form_mapper = {
    Player: CreatePlayer,
    Session: CreateSession,
    Character: CreateCharacter,
    Enemy: CreateEnemy,
    Adventure: CreateAdventure,
    Campaign: CreateCampaign,
    Inventory: CreateInventory,
    Map: CreateMap
}


def home(request):
    if request.user.is_anonymous:
        context = {}
    else:
        context = {
            'characters': Character.objects.filter(owner__user=request.user),
            'adventures': Adventure.objects.all(),
            'campaigns': Campaign.objects.all(),
            'sessions': Session.objects.all(),
            'enemies': Enemy.objects.all(),
            'maps': Map.objects.all(),
            'items': Inventory.objects.all(),
            'has_player': has_free_player(request.user),
        }
    return render(request, 'home.html', context)


@login_required(login_url='/login/')
def new_session(request):
    if request.method == 'POST':
        form = CreateSession(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.success(request, 'Session was created successfully.')
            return redirect('home')
    else:
        form = CreateSession()
    context = {
        'title': 'Create session',
        'form': form,
        'name': 'New session',
        'submit_name': 'Create session'
    }
    return render(request, 'create.html', context)


# @user_passes_test(has_free_player, login_url='/home/')
@login_required(login_url='/login/')
def new_character(request):
    if request.method == 'POST':
        form = CreateCharacter(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            messages.success(request, 'Character was created successfully.')
            return redirect('home')
        else:
            messages.error(request, "Can't create character, invalid form detected")
    else:
        form = CreateCharacter()
        form.fields['owner'].queryset = Player.objects.filter(user=request.user)

    context = {
        'title': 'Create character',
        'form': form,
        'name': 'New character',
        'submit_name': 'Add character'
    }

    return render(request, 'create.html', context)


@login_required(login_url='/login/')
def new_player(request):
    if request.method == 'POST':
        form = CreatePlayer(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()
            messages.success(request, 'Player was created successfully.')
            return redirect('home')
        else:
            messages.error(request, "Can't create player, invalid form detected")
    else:
        form = CreatePlayer()

    context = {
        'title': 'Create player',
        'form': form,
        'name': 'New player',
        'submit_name': 'Add player'
    }

    return render(request, 'create.html', context)


@login_required(login_url='/login/')
def new_map(request):
    if request.method == 'POST':
        form = CreateMap(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.author = request.user
            f.save()
            messages.success(request, 'Map was created successfully.')
            return redirect('home')
        else:
            messages.error(request, "Can't create map, invalid form detected")
    else:
        form = CreateMap()

    context = {
        'title': 'Create map',
        'form': form,
        'name': 'New map',
        'submit_name': 'Add map'
    }
    return render(request, 'create.html', context)


@login_required(login_url='/login')
def details_campaign(request, id, model):
    obj = get_object_or_404(model, id=id)
    return render(request, 'detailed_views/details_campaign.html', {'obj_details': obj})


@login_required(login_url='/login')
def details_map(request, id, model):
    obj = get_object_or_404(model, id=id)
    return render(request, 'detailed_views/details_map.html', {'obj_details': obj})


@login_required(login_url='/login')
def details_player(request, id, model):
    obj = get_object_or_404(model, id=id)
    return render(request, 'detailed_views/details_player.html', {'obj_details': obj})


@login_required(login_url='/login')
def details_character(request, id, model):
    obj = get_object_or_404(model, id=id)
    return render(request, 'detailed_views/details_character.html', {'obj_details': obj})


@login_required(login_url='/login')
def details_session(request, id, model):
    obj = get_object_or_404(model, id=id)
    return render(request, 'detailed_views/details_session.html', {'obj_details': obj})


@login_required(login_url='/login')
def details_enemy(request, id, model):
    obj = get_object_or_404(model, id=id)
    return render(request, 'detailed_views/details_enemy.html', {'obj_details': obj})


@login_required(login_url='/login')
def details_adventure(request, id, model):
    obj = get_object_or_404(model, id=id)
    return render(request, 'detailed_views/details_adventure.html', {'obj_details': obj})


@login_required(login_url='/login')
def details_inventory(request, id, model):
    obj = get_object_or_404(model, id=id)
    return render(request, 'detailed_views/details_inventory.html', {'obj_details': obj})


@login_required(login_url='/home/')
def delete(request, id, model):
    obj = get_object_or_404(model, id=id)
    if request.method == 'POST':
        name = str(obj)
        obj.delete()
        messages.success(request, '{} was deleted.'.format(name))
        return redirect('home')
    return render(request, 'delete.html', {'obj_details': obj})


@login_required(login_url='/home/')
def edit(request, id, model):
    obj = get_object_or_404(model, id=id)
    if request.method == 'POST':
        form = model_form_mapper[model](request.POST, instance=obj)
        if form.is_valid():
            f = form.save()
            messages.success(request, "'{}' was updated successfully.".format(obj))
            return redirect('home')
        else:
            messages.error(request, "Can't update '{}', invalid form detected".format(obj))
    else:
        form = model_form_mapper[model](instance=obj)

    context = {
        'title': 'Edit {}'.format(model.__name__.lower()),
        'form': form,
        'name': 'Edit {}'.format(model.__name__.lower()),
        'submit_name': 'Submit changes'
    }
    return render(request, 'create.html', context)



@login_required(login_url='/login/')
def new_enemy(request):
    if request.method == 'POST':
        form = CreateEnemy(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.author = request.user
            f.save()
            messages.success(request, 'Enemy was created successfully.')
            return redirect('home')
        else:
            messages.error(request, "Can't create enemy, invalid form detected")
    else:
        form = CreateEnemy()

    context = {
        'title': 'Create enemy',
        'form': form,
        'name': 'New enemy',
        'submit_name': 'Add enemy'
    }
    return render(request, 'create.html', context)


Campaign


@login_required(login_url='/login/')
def new_adventure(request):
    if request.method == 'POST':
        form = CreateAdventure(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            messages.success(request, 'Adventure was created successfully.')
            return redirect('home')
        else:
            messages.error(request, "Can't create adventure, invalid form detected")
    else:
        form = CreateAdventure()

    context = {
        'title': 'Create adventure',
        'form': form,
        'name': 'New adventure',
        'submit_name': 'Add adventure'
    }
    return render(request, 'create.html', context)


@login_required(login_url='/login/')
def new_campaign(request):
    if request.method == 'POST':
        form = CreateCampaign(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            messages.success(request, 'Campaign was created successfully.')
            return redirect('home')
        else:
            messages.error(request, "Can't create campaign, invalid form detected")
    else:
        form = CreateCampaign()

    context = {
        'title': 'Create campaign',
        'form': form,
        'name': 'New campaign',
        'submit_name': 'Add campaign'
    }
    return render(request, 'create.html', context)


@login_required(login_url='/login/')
def new_inventory(request):
    if request.method == 'POST':
        form = CreateInventory(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.owner = None
            f.save()
            messages.success(request, 'Item was created successfully.')
            return redirect('home')
        else:
            messages.error(request, "Can't create item, invalid form detected")
    else:
        form = CreateInventory()

    context = {
        'title': 'Create item',
        'form': form,
        'name': 'New item',
        'submit_name': 'Add item'
    }
    return render(request, 'create.html', context)
