from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'


