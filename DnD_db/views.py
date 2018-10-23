from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

from .forms import *
from .models import *


# Create your views here.

def home(request):
    active_sessions = Session.objects.order_by('creation_date')[:3]
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
    attrs = {
        'form': form,
        'name': 'New session',
        'submit_name': 'Create session'
    }
    return render(request, 'create.html', attrs)


@login_required(login_url='/login/')
def new_character(request):
    if request.method == 'POST':
        form = CreateCharacter(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            try:
                post.owner = Player.objects.get(user=request.user)
            except ObjectDoesNotExist:
                raise forms.ValidationError('{} not allowed to create character without being a Player'.format(
                    request.user.username))
            post.save()
            return redirect('home')
    else:
        form = CreateCharacter()

    attrs = {
        'form': form,
        'name': 'New character',
        'submit_name': 'Add character'
    }

    return render(request, 'create.html', attrs)
