from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100, blank=False, default='new player')
    session_part = models.ManyToManyField('Session', blank=True)

    def __str__(self):
        return self.nickname


class Session(models.Model):
    location = models.CharField(max_length=100, blank=False)
    creation_date = models.DateTimeField(default=now)
    creator = models.ForeignKey(Player, on_delete=models.CASCADE, blank=False)
    campaign = models.ForeignKey('Campaign', on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return "{}: {}".format(self.pk, self.location)


class Character(models.Model):
    HB = 'HB'
    KU = 'KU'
    DW = 'DW'
    EL = 'EL'
    HM = 'HM'
    BA = 'BA'
    KR = 'KR'
    RACES = (
        (HB, 'Hobbit'),
        (KU, 'Kuduk'),
        (DW, 'Dwarf'),
        (EL, 'Elf'),
        (HM, 'Human'),
        (BA, 'Barbar'),
        (KR, 'Kroll')
    )

    WA = 'WA'
    FI = 'FI'
    FE = 'FE'
    RA = 'RA'
    ST = 'ST'
    DR = 'DR'
    WI = 'WI'
    SO = 'SO'
    MA = 'MA'
    AL = 'AL'
    TE = 'TE'
    PY = 'PY'
    TH = 'TH'
    RO = 'RO'
    SI = 'SI'
    SPECS = (
        (WA, 'Warrior'),
        (FI, 'Fighter'),
        (FE, 'Fencer'),
        (RA, 'Ranger'),
        (ST, 'Strider'),
        (DR, 'Druid'),
        (WI, 'Wizard'),
        (SO, 'Sorcerer'),
        (MA, 'Mage'),
        (AL, 'Alchemist'),
        (TE, 'Theurg'),
        (PY, 'Pyrofor'),
        (TH, 'Thief'),
        (RO, 'Robber'),
        (SI, 'Sicco'),
    )

    name = models.CharField(max_length=100)
    race = models.CharField(max_length=2, choices=RACES, default=HM)
    speciality = models.CharField(max_length=2, choices=SPECS, default=WA)
    level = models.IntegerField(default=1)
    owner = models.ForeignKey(Player, on_delete=models.CASCADE, blank=False)
    death = models.OneToOneField('CharacterDeath', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class Map(models.Model):
    name = models.CharField(max_length=100)
    author = models.ManyToManyField(Player)

    def __str__(self):
        return self.name


class Enemy(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    author = models.ManyToManyField(Player)

    def __str__(self):
        return self.name


class Adventure(models.Model):
    name = models.CharField(max_length=100)
    difficulty = models.IntegerField()
    purpose = models.TextField()
    location = models.CharField(max_length=100)
    map = models.ManyToManyField(Map, blank=False)
    enemies = models.ManyToManyField(Enemy, blank=True)

    def __str__(self):
        return self.name


class Campaign(models.Model):
    name = models.CharField(max_length=100)
    info = models.TextField()
    adventures = models.ManyToManyField(Adventure, blank=False)

    def __str__(self):
        return self.name


class CharacterDeath(models.Model):
    time = models.DateTimeField(default=now)
    place = models.ForeignKey('Map', on_delete=models.CASCADE, blank=False)


class Inventory(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    owner = models.ForeignKey(Character, blank=True, null=True, on_delete=models.PROTECT)
