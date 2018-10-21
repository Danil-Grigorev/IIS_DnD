from django import forms

from .models import *


class CreateSession(forms.ModelForm):
    class Meta:
        model = Session
        widgets = {'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter location"})}

        fields = ['location']
