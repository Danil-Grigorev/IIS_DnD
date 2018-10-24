from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect

from .forms import *
from .tests import *


# Create your views here.

def home(request):
    active_sessions = Session.objects.order_by('creation_date')
    context = {
        'active_sessions': active_sessions,
    }
    return render(request, 'home.html', context)


@login_required(login_url='/login/')
def new_session(request):
    if request.method == 'POST':
        form = CreateSession(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
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


@user_passes_test(has_free_player, login_url='/home/')
@login_required(login_url='/login/')
def new_character(request):
    if request.method == 'POST':
        form = CreateCharacter(request.POST, initial={'owner': Player.objects.get(user=request.user)})
        if form.is_valid():
            f = form.save(commit=False)
            f.owner = Player.objects.get(user=request.user)
            f.save()
            return redirect('home')
    else:
        form = CreateCharacter()

    context = {
        'title': 'Create character',
        'form': form,
        'name': 'New character',
        'submit_name': 'Add character'
    }

    return render(request, 'create.html', context)


def new_player(request):
    if request.method == 'POST':
        form = CreatePlayer(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()
            return redirect('home')
    else:
        form = CreatePlayer()

    context = {
        'title': 'Create player',
        'form': form,
        'name': 'New player',
        'submit_name': 'Add player'
    }

    return render(request, 'create.html', context)
