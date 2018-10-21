from django.shortcuts import render


# Create your views here.

def home(request):
    return render(request, 'home.html', {})


def new_session(request):
    return render(request, )
