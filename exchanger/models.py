from django.db import models
from django.contrib.auth.models import AbstractBaseUser

import os


class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)
    can_act = models.BooleanField()
    max_invites = models.IntegerField()
    needs_moderation = models.BooleanField()
    is_moderator = models.BooleanField()
    can_bless = models.BooleanField()

    def __str__(self):
        return self.name

class User(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    access = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='users')

    def __str__(self):
        return self.username + ' [' + str(self.access) + ']'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['access']

class Invite(models.Model):
    emitent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitees')
    text = models.CharField(max_length=128, unique=True)
    newbie = models.OneToOneField(User, blank=True, null=True, related_name='invite')

    def __str__(self):
        return self.text + ' from ' + self.emitent.username

class Provider(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=2048)

    def _get_picture_path(instance, filename):
        return os.path.join('images', 'providers', str(instance.id), filename)
    picture = models.ImageField(upload_to=_get_picture_path, blank=True, null=True)

    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Campaign(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=2048)
    provider = models.ForeignKey(Provider, related_name='campaigns')
    ref_type = models.IntegerField(choices=((0, "Code"), (1, "Link")))
    value_re = models.CharField(max_length=255)

    def __str__(self):
        return self.provider.name + ' ' + self.name

class Promo(models.Model):
    adder = models.ForeignKey(User, related_name='promos')
    campaign = models.ForeignKey(Campaign, related_name='promos')
    value = models.CharField(max_length=1024)

    def __str__(self):
        return str(self.campaign) + ' ' + self.value + ' from ' + self.adder.username
