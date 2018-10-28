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


#test


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


class CreateEnemy(forms.ModelForm):
    class Meta:
        model = Enemy
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enemy name'}),
            'type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enemy description'}),
            'author': forms.SelectMultiple(attrs={'class': 'form-control'})
        }
        fields = ['name', 'type', 'author']


class CreateAdventure(forms.ModelForm):
    class Meta:
        model = Adventure
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adventure name'}),
            'difficulty': forms.NumberInput(),
            'purpose': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adventure name'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Map name'}),
            'map': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Map name'}),
            'enemies': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Enemy name'}),

        }
        fields = ['name', 'difficulty', 'purpose', 'location', 'map', 'enemies']