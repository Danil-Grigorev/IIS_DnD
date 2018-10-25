from django import forms

from .models import *


class CreateSession(forms.ModelForm):
    class Meta:
        model = Session
        widgets = {
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter location"}),
            'campaign': forms.Select(attrs={'class': 'form-control', 'placeholder': "Enter location"})
        }
        fields = ['location', 'campaign']

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
        }
        fields = ['name', 'race', 'speciality']


class CreatePlayer(forms.ModelForm):
    class Meta:
        model = Player
        widgets = {
            'nickname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pick a nickname'})
        }
        fields = ['nickname']


class CreateMap(forms.ModelForm):
    class Meta:
        model = Map
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Map name'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Map description'}),
            'author': forms.SelectMultiple(attrs={'class': 'form-control'})
        }
        fields = ['name', 'description', 'author']

    # def save(self, user=None, commit=True):
    #     s = Map()
    #     if user:
    #         s.author.add(user)
    #     if commit:
    #         s.save()
    #     return s
