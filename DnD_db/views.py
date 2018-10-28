from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import *
from .tests import *


# Create your views here.

def home(request):
    active_sessions = Session.objects.order_by('creation_date')
    if request.user.is_anonymous:
        context = {}
    else:
        context = {
            'characters': Character.objects.filter(owner__user=request.user),
            'active_sessions': active_sessions,
            'has_player': has_free_player(request.user),
            'is_author': created_maps(request.user),
            'is_session_leader': created_sessions(request.user),
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
            f.save()
            messages.success(request, 'Map was created successfully.')
            return redirect('home')
        else:
            messages.error(request, "Can't create map, invalid form detected")
    else:
        form = CreateMap()
        form.fields['author'].queryset = Player.objects.filter(user=request.user)

    context = {
        'title': 'Create map',
        'form': form,
        'name': 'New map',
        'submit_name': 'Add map'
    }
    return render(request, 'create.html', context)


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


@login_required(login_url='/home/')
def delete(request, id, model):
    obj = get_object_or_404(model, id=id)
    if request.method == 'POST':
        name = str(obj)
        obj.delete()
        messages.success(request, '{} was deleted.'.format(name))
        return redirect('home')
    return render(request, 'delete.html', {'obj_details': obj})


@login_required(login_url='/login/')
def new_enemy(request):
    if request.method == 'POST':
        form = CreateEnemy(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            messages.success(request, 'Enemy was created successfully.')
            return redirect('home')
        else:
            messages.error(request, "Can't create enemy, invalid form detected")
    else:
        form = CreateEnemy()
        form.fields['author'].queryset = Player.objects.filter(user=request.user)

    context = {
        'title': 'Create enemy',
        'form': form,
        'name': 'New enemy',
        'submit_name': 'Add enemy'
    }
    return render(request, 'create.html', context)

