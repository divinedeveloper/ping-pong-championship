from django.db import transaction
from django.conf import settings
from api.models import Player, Championship, Game, PlayerToken, Referee
from api.custom_exceptions import CustomApiException
from rest_framework import status
from random import randint, sample
from django.db.models import Q
import os
import json

from django.db.models import Lookup
from django.db.models.fields import Field

@Field.register_lookup
class NotEqual(Lookup):
	lookup_name = 'ne'

	def as_sql(self, qn, connection):
		lhs, lhs_params = self.process_lhs(qn, connection)
		rhs, rhs_params = self.process_rhs(qn, connection)
		params = lhs_params + rhs_params
		return '%s <> %s' % (lhs, rhs), params

class Services():
	def __init__(self):
		return

	def referee_instruction(self, championship, game, player_one, player_two, notification, instruction):

		Referee(championship = championship, game = game, player_one_detail = player_one, player_two_detail = player_two, 
			notification = notification, next_instruction = instruction).save()

		return

	# def login(self, name):
	# 	#save referee instructions to toss
	# 	try:
	# 		selected_player = Player.objects.get(name__exact = name, status__exact= settings.PLAYER_STATUS['Selected'])

	# 		player_token = PlayerToken.objects.get(player__exact = selected_player)

	# 		if player_token:
	# 			return player_token

	# 	except Player.DoesNotExist:
	# 		raise CustomApiException("Player {0} was not found".format(name), status.HTTP_404_NOT_FOUND)

	# 	except PlayerToken.DoesNotExist:
	# 		championship = Championship.objects.get(status__exact= settings.CHAMPIONSHIP_STATUS['Started'])

	# 		if not championship:
	# 			raise CustomApiException("Please register players first", status.HTTP_400_BAD_REQUEST)

	# 		drawn_games_query_list = Game.objects.filter(Q(championship__exact = championship.id) & Q(status__exact= settings.GAME_STATUS['Drawn']))
	# 		drawn_games = list(drawn_games_query_list)

	# 		if not drawn_games:
	# 			raise CustomApiException("No games to play", status.HTTP_400_BAD_REQUEST)

	# 		game_to_play = drawn_games[0]

	# 		if not (game_to_play.player_one == selected_player or game_to_play.player_two == selected_player):
	# 			raise CustomApiException("Please login as {0} or {1}".format(game_to_play.player_one.name, game_to_play.player_two.name), status.HTTP_400_BAD_REQUEST)

	# 		#check if token exists for any of the players in current game
	# 		#if exists then raise exception that name is already loged in
	# 		player_token_exists = PlayerToken.objects.get(Q(player__exact = game_to_play.player_one) | 
	# 			Q(player__exact = game_to_play.player_two))

	# 		if player_token_exists:
	# 			raise CustomApiException("Player {0} has already logged in for this game".format(player_token_exists.player.name), 
	# 				status.HTTP_400_BAD_REQUEST)

	# 		PlayerToken(player= selected_player).save()

	# 		player_token = PlayerToken.objects.get(player__exact = selected_player)
	# 		return player_token

	@transaction.atomic
	def login(self, name):
		selected_player_query_set = Player.objects.filter(name__exact = name, status__exact= settings.PLAYER_STATUS['Selected'])

		if selected_player_query_set.count() == 0:
			raise CustomApiException("Player {0} was not found or is shutdown".format(name), status.HTTP_404_NOT_FOUND)

		selected_player = selected_player_query_set[0]

		player_token_query_set = PlayerToken.objects.filter(player__exact = selected_player)

		if player_token_query_set.count() > 0:
			return player_token_query_set[0]

		championship_query_set = Championship.objects.filter(status__exact= settings.CHAMPIONSHIP_STATUS['Started'])

		if championship_query_set.count() == 0:
			raise CustomApiException("Please register players first", status.HTTP_400_BAD_REQUEST)

		championship = championship_query_set[0]

		drawn_games_query_list = Game.objects.filter(Q(championship__exact = championship.id) & Q(status__exact= settings.GAME_STATUS['Drawn']))
		drawn_games = list(drawn_games_query_list)

		if not drawn_games:
			raise CustomApiException("No games to play", status.HTTP_400_BAD_REQUEST)

		game_to_play = drawn_games[0]

		if not (game_to_play.player_one == selected_player or game_to_play.player_two == selected_player):
			raise CustomApiException("Please login as {0} or {1}".format(game_to_play.player_one.name, game_to_play.player_two.name), status.HTTP_400_BAD_REQUEST)

		#check if token exists for any of the players in current game
		#if exists then raise exception that name is already loged in
		player_token_exists = PlayerToken.objects.filter(Q(player__exact = game_to_play.player_one) | 
			Q(player__exact = game_to_play.player_two))

		if player_token_exists.count() > 0:
			raise CustomApiException("Player {0} has already logged in for this game".format(player_token_exists[0].player.name), 
				status.HTTP_400_BAD_REQUEST)

		PlayerToken(player= selected_player).save()

		player_token = PlayerToken.objects.get(player__exact = selected_player)

		#save referee instructions to toss
		notification = settings.LOGIN_NOTIFICATION.format(name)
		instruction = settings.TOSS_INSTRUCTION.format(name, game_to_play.player_one.name, game_to_play.player_two.name)

		self.referee_instruction(championship,game_to_play,game_to_play.player_one, game_to_play.player_two, 
			notification, instruction)

		return player_token
				
			
			






