# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
import uuid

# Create your models here.

class Player(models.Model):
    name = models.CharField(blank = False, max_length = 20, unique = True)
    defence_set_length = models.SmallIntegerField(blank = False)
    status = models.CharField(blank = False, max_length = 25)
    role = models.CharField(blank = False, max_length = 20)
    date_created = models.DateTimeField(default = timezone.now)

class Championship(models.Model):
    champion = models.ForeignKey(Player, null = True, blank= True)
    status = models.CharField(blank = False, max_length = 25, default = "Ended")
    date_created = models.DateTimeField(default = timezone.now)

class Game(models.Model):
	championship = models.ForeignKey(Championship)
	player_one = models.ForeignKey(Player, related_name = 'participant_one')
	player_two = models.ForeignKey(Player, related_name = 'participant_two')
	player_one_score = models.SmallIntegerField(blank = False)
	player_two_score = models.SmallIntegerField(blank = False)
	winner = models.ForeignKey(Player, related_name = 'match_winner', null = True, blank = True)
	game_type = models.CharField(blank = False, max_length = 10)
	status = models.CharField(blank = False, max_length = 20)
	date_created = models.DateTimeField(default = timezone.now)

class PlayerToken(models.Model):
    player = models.ForeignKey(Player)
    token = models.UUIDField(default = uuid.uuid4, editable = False)
    date_created = models.DateTimeField(default = timezone.now)

class Referee(models.Model):
	championship = models.ForeignKey(Championship)
	game = models.ForeignKey(Game, null = True, blank= True)
	player_one_detail = models.ForeignKey(Player, related_name = 'details_player_one', null = True, blank = True)
	player_two_detail = models.ForeignKey(Player, related_name = 'details_player_two', null = True, blank = True)
	notification = models.CharField(blank = False, max_length = 200)
	next_instruction = models.CharField(blank = False, max_length = 200)
	date_created = models.DateTimeField(default = timezone.now)
