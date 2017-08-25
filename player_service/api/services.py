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

	
	@transaction.atomic
	def offensive_move(self, random_number):
		current_game_query_set = Game.objects.filter(status__exact= settings.GAME_STATUS['InProgress'])
		if current_game_query_set.count() == 0:
			raise CustomApiException("Please start game first", status.HTTP_400_BAD_REQUEST)

		player_token_query_set = PlayerToken.objects.filter(token__isnull = False)

		if player_token_query_set.count() == 0:
			raise CustomApiException("Player not logged in", status.HTTP_401_UNAUTHORIZED)

		player_token = player_token_query_set[0]

		if player_token.player.role != settings.PLAYER_ROLE['Offensive']:
			raise CustomApiException("Please play Defensive move", status.HTTP_403_FORBIDDEN)


		current_game = current_game_query_set[0]

		if current_game.player_one != player_token.player:
			opponent = current_game.player_one

		if current_game.player_two != player_token.player:
			opponent = current_game.player_two

		defense_array_move = sample(range(1,11), opponent.defence_set_length)

		self.judge_move_winner(current_game, random_number, defense_array_move)

		if current_game.player_one_score == 5 or current_game.player_two_score == 5:
			self.declare_winner(current_game, player_token)


		referee = Referee.objects.latest('date_created')

		return referee

	@transaction.atomic
	def defensive_move(self, defense_array_move):
		#check if points more than 5 that player wins, 1 winner, other looser, 
			#save winner, game status->Done.
			#delete player token of logged in user

			#save winner referee  instructions
		
		#return 

		current_game_query_set = Game.objects.filter(status__exact= settings.GAME_STATUS['InProgress'])
		if current_game_query_set.count() == 0:
			raise CustomApiException("Please start game first", status.HTTP_400_BAD_REQUEST)

		player_token_query_set = PlayerToken.objects.filter(token__isnull = False)

		if player_token_query_set.count() == 0:
			raise CustomApiException("Player not logged in", status.HTTP_401_UNAUTHORIZED)

		player_token = player_token_query_set[0]

		if player_token.player.role != settings.PLAYER_ROLE['Defensive']:
			raise CustomApiException("Please play Offensive move", status.HTTP_403_FORBIDDEN)

		if len(defense_array_move) != player_token.player.defence_set_length:
			raise CustomApiException("Please provide defense array of {0} length only".format(str(player_token.player.defence_set_length)), 
				status.HTTP_400_BAD_REQUEST)

		offensive_move = randint(1,10)

		current_game = current_game_query_set[0]

		self.judge_move_winner(current_game, offensive_move, defense_array_move)

		if current_game.player_one_score == 5 or current_game.player_two_score == 5:
			self.declare_winner(current_game, player_token)

		referee = Referee.objects.latest('date_created')

		return referee


	@transaction.atomic
	def judge_move_winner(self, current_game, offensive_move, defense_array_move):
		#check if that number exists in user given array
		# if yes defense  won , defense points increment and switch roles
		#if no then offense won, offense points increment

		#save referee instructions
		player_one = current_game.player_one
		player_two = current_game.player_two

		if player_one.role == settings.PLAYER_ROLE['Offensive']:
			if offensive_move not in defense_array_move:
				#increment point of player one
				# one type will be offensive
				#two type will be defensive
				self.player_one_wins_move(current_game, player_two, player_one)

			else:
				#increment point of player TWO
				# two type will be offensive
				#one type will be defensive
				self.player_two_wins_move(current_game, player_two, player_one)
		else:
			if offensive_move not in defense_array_move:
				#increment point of player two
				# two type will be offensive
				#one type will be defensive
				self.player_two_wins_move(current_game, player_two, player_one)

			else:
				#increment point of player One
				# one type will be offensive
				#two type will be defensive
				self.player_one_wins_move(current_game, player_two, player_one)


	@transaction.atomic
	def player_two_wins_move(self,current_game, player_two, player_one):
		current_game.player_two_score += 1
		player_two.role = settings.PLAYER_ROLE['Offensive']
		player_one.role = settings.PLAYER_ROLE['Defensive']

		notification = settings.MOVE_NOTIFICATION.format(player_two.name)
		instruction = settings.MOVE_INSTRUCTION.format(player_two.name,
			player_one.name, player_one.defence_set_length)

		player_two.save()
		player_one.save()
		current_game.save()

		self.referee_instruction(current_game.championship, current_game, player_one, player_two, 
			notification, instruction)




	@transaction.atomic
	def player_one_wins_move(self,current_game, player_two, player_one):
		current_game.player_one_score += 1
		player_one.role = settings.PLAYER_ROLE['Offensive']
		player_two.role = settings.PLAYER_ROLE['Defensive']

		notification = settings.MOVE_NOTIFICATION.format(player_one.name)
		instruction = settings.MOVE_INSTRUCTION.format(player_one.name,
			player_two.name, player_two.defence_set_length)

		player_two.save()
		player_one.save()
		current_game.save()

		self.referee_instruction(current_game.championship, current_game, player_one, player_two, 
			notification, instruction)


	def declare_winner(self, current_game, player_token):

		if current_game.player_one_score > current_game.player_two_score:
			current_game.player_one.status = settings.PLAYER_STATUS['Winner']
			current_game.player_two.status = settings.PLAYER_STATUS['Looser']

			current_game.winner = current_game.player_one
			current_game.status = settings.GAME_STATUS['Done']

		else:
			current_game.player_two.status = settings.PLAYER_STATUS['Winner']
			current_game.player_one.status = settings.PLAYER_STATUS['Looser']

			current_game.winner = current_game.player_two
			current_game.status = settings.GAME_STATUS['Done']

		
		current_game.player_one.role = settings.PLAYER_ROLE["N/A"]
		current_game.player_two.role = settings.PLAYER_ROLE["N/A"]
		current_game.player_one.save()
		current_game.player_two.save()
		current_game.save()

		player_token.delete()


		drawn_games = Game.objects.filter(Q(championship__exact = current_game.championship.id) & Q(status__exact= settings.GAME_STATUS['Drawn']))

		if not drawn_games:
			if current_game.game_type != "Final":
				notification = settings.WINNER_NOTIFICATION.format(current_game.winner.name)
				instruction = settings.SHUTDOWN_INSTRUCTION
			else:
				#save championship winner in championship
				#shutdown last 2 players
				#championship status Ended
				current_game.championship.champion = current_game.winner

				Player.objects.filter(status__ne = settings.PLAYER_STATUS['Shutdown']).update(status = settings.PLAYER_STATUS['Shutdown'],
					role= settings.PLAYER_ROLE['N/A'])

				current_game.championship.status = settings.CHAMPIONSHIP_STATUS["Ended"]

				current_game.championship.save()

				notification = settings.CHAMPIONSHIP_WINNER_NOTIFICATION.format(current_game.winner.name)
				instruction = settings.NEXT_CHAMPIONSHIP_INSTRUCTION

		else:
			next_game = drawn_games[0]
			notification = settings.WINNER_NOTIFICATION.format(current_game.winner.name)
			instruction = settings.WINNER_INSTRUCTION.format(next_game.player_one.name, next_game.player_two.name)

		self.referee_instruction(current_game.championship, current_game, current_game.player_one, current_game.player_two, 
			notification, instruction)	


		















			





				
			
			






