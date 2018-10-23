from django import forms

from .models import *


class CreateSession(forms.ModelForm):
    class Meta:
        model = Session
        widgets = {'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter location"})}
        fields = ['location']

    #
    # name = models.CharField(max_length=100)
    # race = models.CharField(max_length=2, choices=RACES, default=HM)
    # speciality = models.CharField(max_length=2, choices=SPECS, default=WA)
    # level = models.IntegerField(default=0)
    # owner = models.OneToOneField(Player, on_delete=models.CASCADE)


class CreateCharacter(forms.ModelForm):
    class Meta:
        model = Character
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Character name'}),
            'race': forms.Select(attrs={'class': 'form-control'}),
            'speciality': forms.Select(attrs={'class': 'form-control'}),
            'owner': forms.Select(attrs={'class': 'form-control'})
        }
        fields = ['name', 'race', 'speciality', 'owner']
