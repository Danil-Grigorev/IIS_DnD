from django import forms

from .models import *
from .tests import get_free_players


class TakePartS(forms.Form):
    class Meta:
        fields = ('session', 'player')

    def __init__(self, profile, sess_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sess_id = sess_id
        self.fields['player'] = forms.ModelChoiceField(
            queryset=get_free_players(profile),
            widget=forms.Select(attrs={'class': 'form-control', 'placeholder': "Choose session"})
        )

    def save(self):
        data = self.cleaned_data
        player = data['player']
        player.session_part = Session.objects.get(id=self.sess_id)
        player.save()


class CreateMessage(forms.ModelForm):
    def __init__(self, profile, sess, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.profile = profile
        self.sess = sess

    class Meta:
        model = Message
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter message"}),
            'type': forms.Select(attrs={'class': 'form-control', 'placeholder': "Select type"})
        }
        fields = ['text', 'type']

    def save(self, commit=True):
        s = super().save(commit=False)
        s.author = self.profile
        s.session = self.sess
        super().save(commit)


class CreateSession(forms.ModelForm):

    def __init__(self, profile, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].queryset = Player.objects.filter(user=profile)

    class Meta:
        model = Session
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter title"}),
            'campaign': forms.Select(attrs={'class': 'form-control', 'placeholder': "Choose campaign"}),
            'author': forms.Select(attrs={'class': 'form-control', 'placeholder': "Choose creator"})

        }
        fields = ['title', 'campaign', 'author']
        labels = {'author': 'leader'}


class CreateCharacter(forms.ModelForm):

    def __init__(self, profile, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].queryset = Player.objects.filter(user=profile)

    class Meta:
        model = Character
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Character name'}),
            'race': forms.Select(attrs={'class': 'form-control'}),
            'speciality': forms.Select(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'})
        }
        fields = ['name', 'race', 'speciality', 'author']
        labels = {'author': 'related player'}


class CreatePlayer(forms.ModelForm):

    def __init__(self, profile, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.profile = profile

    class Meta:
        model = Player
        widgets = {
            'nickname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pick a nickname'})
        }
        fields = ['nickname']

    def save(self, commit=True):
        s = super().save(commit=False)
        s.user = self.profile
        super().save()


class CreateMap(forms.ModelForm):

    def __init__(self, profile, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.profile = profile

    class Meta:
        model = Map
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Map name'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Map description'}),
        }
        fields = ['name', 'description']

    def save(self, commit=True):
        s = super().save(commit=False)
        s.author = self.profile
        super().save()


class CreateEnemy(forms.ModelForm):

    def __init__(self, profile, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.profile = profile

    class Meta:
        model = Enemy
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enemy name'}),
            'type': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Enemy description'}),
        }
        fields = ['name', 'type']

    def save(self, commit=True):
        s = super().save(commit=False)
        s.author = self.profile
        super().save()


class CreateAdventure(forms.ModelForm):

    def __init__(self, profile, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.profile = profile

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

    def save(self, commit=True):
        s = super().save(commit=False)
        s.author = self.profile
        super().save()


class CreateCampaign(forms.ModelForm):

    def __init__(self, profile, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.profile = profile

    class Meta:
        model = Campaign
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Campaign name'}),
            'info': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Campaign description'}),
            'adventures': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Adventure name'}),
        }
        fields = ['name', 'info', 'adventures']

    def save(self, commit=True):
        s = super().save(commit=False)
        s.author = self.profile
        super().save()


class CreateInventory(forms.ModelForm):

    def __init__(self, profile, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.profile = profile

    class Meta:
        model = Inventory
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item name'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
        }
        fields = ['name', 'type', ]

    def save(self, commit=True):
        s = super().save(commit=False)
        s.author = self.profile
        s.owner = None
        super().save()
