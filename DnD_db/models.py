from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, \
    MaxValueValidator, validate_slug, MinLengthValidator, MaxLengthValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import reverse
from django.utils.timezone import now


class Message(models.Model):
    TA = 'Task'
    AC = 'Action'
    CO = 'Comment'
    TYPES = ((AC, AC), (CO, CO), (TA, TA))

    text = models.TextField()
    type = models.CharField(max_length=7, blank=False, null=False, choices=TYPES, default=AC)
    date_posted = models.DateTimeField(default=now)
    author = models.ForeignKey('Player', on_delete=models.SET_NULL, blank=False, null=True)
    session = models.ForeignKey('Session', on_delete=models.CASCADE, blank=False, null=True)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        text = self.text[:20] + '...' if len(self.text) > 20 else self.text
        return '{} - {}'.format(self.author, text, self.date_posted)


class Profile(models.Model):
    PL = 'Player'
    AU = 'Author'
    PJ = 'Session leader'
    roles = ((PL, PL), (AU, AU), (PJ, PJ))
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    role = models.CharField(max_length=14, blank=False, null=False, choices=roles, default=PL)
    invitations = models.ManyToManyField('Session', through='Player', blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def set_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


class Player(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    nickname = models.CharField(max_length=30, blank=False, default='new_player', unique=True,
                                validators=[
                                    MinLengthValidator(4),
                                    MaxLengthValidator(30),
                                    validate_slug
                                ])
    session_part = models.ForeignKey('Session', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.nickname

    def get_absolute_url(self):
        return '/player_details/{}'.format(self.id)


class Session(models.Model):
    title = models.CharField(max_length=60, blank=False, default='Title for session', unique=True,
                             validators=[
                                 MinLengthValidator(4),
                                 MaxLengthValidator(60)
                             ])
    creation_date = models.DateTimeField(default=now)
    author = models.OneToOneField(Player, on_delete=models.CASCADE, blank=False, null=True)
    campaign = models.ForeignKey('Campaign', on_delete=models.CASCADE, blank=False, null=True)

    def __str__(self):
        return '{}'.format(self.title)

    def get_absolute_url(self):
        return reverse('detailed_session', kwargs={'id': self.id})

    def get_participator_url(self):
        return reverse('view_session', kwargs={'sess_id': self.id})


class Character(models.Model):
    HB = 'Hobbit'
    KU = 'Kuduk'
    DW = 'Dwarf'
    EL = 'Elf'
    HM = 'Human'
    BA = 'Barbar'
    KR = 'Kroll'
    RACES = (
        (HB, HB),
        (KU, KU),
        (DW, DW),
        (EL, EL),
        (HM, HM),
        (BA, BA),
        (KR, KR),
    )

    WA = 'Warrior'
    FI = 'Fighter'
    FE = 'Fencer'
    RA = 'Ranger'
    ST = 'Strider'
    DR = 'Druid'
    WI = 'Wizard'
    SO = 'Sorcerer'
    MA = 'Mage'
    AL = 'Alchemist'
    TE = 'Theurg'
    PY = 'Pyrofor'
    TH = 'Thief'
    RO = 'Robber'
    SI = 'Sicco'
    SPECS = (
        (WA, WA),
        (FI, FI),
        (FE, FE),
        (RA, RA),
        (ST, ST),
        (DR, DR),
        (WI, WI),
        (SO, SO),
        (MA, MA),
        (AL, AL),
        (TE, TE),
        (PY, PY),
        (TH, TH),
        (RO, RO),
        (SI, SI),
    )

    name = models.CharField(max_length=30, unique=True, default='New_character',
                            validators=[
                                MinLengthValidator(4),
                                MaxLengthValidator(30),
                                validate_slug
                            ])
    race = models.CharField(max_length=6, choices=RACES, default=HM)
    speciality = models.CharField(max_length=9, choices=SPECS, default=WA)
    level = models.IntegerField(default=1,
                                validators=[
                                    MinValueValidator(1),
                                    MaxValueValidator(99)
                                ])
    author = models.ForeignKey(Player, on_delete=models.CASCADE, blank=False, null=True)
    death = models.OneToOneField('CharacterDeath', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detailed_character', kwargs={'id': self.id})


class Map(models.Model):
    name = models.CharField(max_length=30, default='New_map', unique=True,
                            validators=[
                                MinLengthValidator(4),
                                MaxLengthValidator(30)
                            ])
    description = models.TextField(default='Some description')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=False, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detailed_map', kwargs={'id': self.id})


class Enemy(models.Model):
    DE = 'Demon'
    DR = 'Dragon'
    SN = 'Snake'
    IN = 'Insect'
    HU = 'Humanoid'
    MA = 'Magical'
    ST = 'Statues'
    CR = 'Creature'
    ENEMIES = (
        (DE, DE),
        (DR, DR),
        (SN, SN),
        (IN, IN),
        (HU, HU),
        (MA, MA),
        (ST, ST),
        (CR, CR),
    )
    name = models.CharField(max_length=30, unique=True, blank=False, default='New_enemy',
                            validators=[
                                MinLengthValidator(4),
                                MaxLengthValidator(30),
                            ])
    type = models.CharField(max_length=8, blank=False, choices=ENEMIES, default=DE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=False, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detailed_enemy', kwargs={'id': self.id})


class Adventure(models.Model):
    name = models.CharField(max_length=60, unique=True, default='New_adventure',
                            validators=[
                                MinLengthValidator(4),
                                MaxLengthValidator(60)
                            ])
    difficulty = models.IntegerField(default=1,
                                     validators=[
                                         MaxValueValidator(10),
                                         MinValueValidator(1),
                                     ])
    purpose = models.TextField(default='New_purpose')
    location = models.CharField(max_length=30, default='Some location',
                                validators=[
                                    MinLengthValidator(4),
                                    MaxLengthValidator(30),
                                ])
    map = models.ManyToManyField(Map, blank=False)
    enemies = models.ManyToManyField(Enemy, blank=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=False, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detailed_adventure', kwargs={'id': self.id})


class Campaign(models.Model):
    name = models.CharField(max_length=30, unique=True, default='New_campaign',
                            validators=[
                                MinLengthValidator(4),
                                MaxLengthValidator(30),
                            ])
    info = models.TextField(default='Campaign info', blank=False)
    adventures = models.ManyToManyField(Adventure, blank=False)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=False, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detailed_campaign', kwargs={'id': self.id})


# TODO: reference to character
class CharacterDeath(models.Model):
    time = models.DateTimeField(default=now)
    place = models.ForeignKey('Map', on_delete=models.CASCADE, blank=False, null=True)


class Inventory(models.Model):
    WP = 'Weapon'
    AR = 'Armor'
    FO = 'Food'
    PO = 'Potion'
    TO = 'Tool'
    OT = 'Other'

    TYPES = (
        (WP, WP),
        (AR, AR),
        (FO, FO),
        (PO, PO),
        (TO, TO),
        (OT, OT),
    )
    name = models.CharField(max_length=30, default='New_item',
                            validators=[
                                MinLengthValidator(4),
                                MaxLengthValidator(30),
                            ])
    type = models.CharField(max_length=6, blank=False, choices=TYPES, default=WP)
    owner = models.ForeignKey(Character, blank=True, null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=False, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detailed_inventory', kwargs={'id': self.id})
