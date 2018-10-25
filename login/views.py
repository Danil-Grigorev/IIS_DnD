from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.views import generic


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/sign_up.html'


class Login(generic.CreateView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/login.html'
