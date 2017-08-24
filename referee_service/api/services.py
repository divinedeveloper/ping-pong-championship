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

	def referee_instructions(self):
		try:
			referee = Referee.objects.latest('date_created')

		except Referee.DoesNotExist as e:
				raise CustomApiException("Referee instructions were not found", status.HTTP_404_NOT_FOUND)

		return referee

	@transaction.atomic
	def player_registration(self):
		#check if players exists in db, set status as Registered
		# if not load players from file and save in db as Registered.
		self.championship_registration()

		if Player.objects.count() == 0:
			try:
				BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
				players_data_file =  os.path.join(BASE_DIR, settings.PLAYER_DATA_FILE_NAME)

				with open(players_data_file) as json_file:
					players_data_list = json.load(json_file)

				for players_data in players_data_list:
					player = Player(name = players_data['player_name'] ,defence_set_length = players_data['player_defence_set_length'],
						status= settings.PLAYER_STATUS['Registered'],role= settings.PLAYER_ROLE['N/A']).save()
			except IOError as e:
				raise CustomApiException("Could not read file: "+settings.PLAYER_DATA_FILE_NAME, status.HTTP_503_SERVICE_UNAVAILABLE)

		else:
			player_not_shutdown = Player.objects.filter(status__ne= settings.PLAYER_STATUS['Shutdown'])

			if len(player_not_shutdown) > 0:
				raise CustomApiException("Registration can only be done once current championship ends.", status.HTTP_403_FORBIDDEN)

			updated_players_list = Player.objects.all().update(status= settings.PLAYER_STATUS['Registered'],
				role= settings.PLAYER_ROLE['N/A'])

		players = Player.objects.all()
		current_championship = Championship.objects.get(status__exact= settings.CHAMPIONSHIP_STATUS['Started'])
		
		#send notification and next_instruction to referee
		self.referee_instruction(current_championship,None,None,None,settings.REGISTERED_NOTIFICATION, settings.DRAW_GAMES_INSTRUCTION)

		return (players, current_championship)

	def championship_registration(self):

		championships = Championship.objects.filter(status__exact= settings.CHAMPIONSHIP_STATUS['Started'])

		if len(championships) > 0:
			raise CustomApiException("Registration can only be done once current championship ends.", status.HTTP_403_FORBIDDEN)

		Championship(status= settings.CHAMPIONSHIP_STATUS['Started']).save()

	def referee_instruction(self, championship, game, player_one, player_two, notification, instruction):

		Referee(championship = championship, game = game, player_one_detail = player_one, player_two_detail = player_two, 
			notification = notification, next_instruction = instruction).save()

		return



	@transaction.atomic
	def draw_games(self):
		championship = Championship.objects.get(status__exact= settings.CHAMPIONSHIP_STATUS['Started'])

		if not championship:
			raise CustomApiException("Please register players first", status.HTTP_400_BAD_REQUEST)

		remaining_games = Game.objects.filter(Q(championship__exact = championship.id) & Q(status__exact= settings.GAME_STATUS['Drawn']))

		if len(remaining_games) > 0:
			raise CustomApiException("Please complete remaining games of this championship", status.HTTP_400_BAD_REQUEST)

		players_query_list = Player.objects.filter(Q(status__ne= settings.PLAYER_STATUS['Looser']) & 
			Q(status__ne= settings.PLAYER_STATUS['Shutdown']))

		players_list = list(players_query_list)

		if len(players_list) < 2:
			raise CustomApiException("Minimum 2 active players are needed to draw a game", status.HTTP_400_BAD_REQUEST)

		game_type = None
		if len(players_list) > 4:
			game_type = "Knockout"
		elif len(players_list) == 4:
			game_type = "Semi-Final"
		elif len(players_list) == 2:
			game_type = "Final"

		while len(players_list) >= 2:
			player_one = players_list.pop(randint(0, len(players_list)-1 ))
			player_two = players_list.pop(randint(0, len(players_list)-1 ))

			selected_status = settings.PLAYER_STATUS['Selected']
			player_role = settings.PLAYER_ROLE["N/A"]
			player_one.status = selected_status
			player_one.role = player_role
			player_one.save()

			player_two.status = selected_status
			player_two.role = player_role
			player_two.save()

			Game(championship = championship, player_one = player_one, player_two = player_two,
				player_one_score = 0, player_two_score = 0, game_type = game_type, 
				status = settings.GAME_STATUS['Drawn']).save()

		games_list = Game.objects.filter(Q(championship__exact = championship.id) & Q(status__exact= settings.GAME_STATUS['Drawn']))

		#send notification and next_instruction to referee
		notification = settings.DRAW_GAMES_NOTIFICATION.format(len(games_list))
		instruction = settings.PLAYER_LOGIN_INSTRUCTION.format(games_list[0].player_one.name, games_list[0].player_two.name)
		self.referee_instruction(championship,games_list[0],games_list[0].player_one, games_list[0].player_two, 
			notification, instruction)

		return games_list

	@transaction.atomic
	def choose_roles_for_players(self, game_id):
		#get game by Drawn status
		#randint(1,2), if 1 player_one offensive and player two defensive, viceversa
		#set player status as Playing
		#set game status as InProgress
		#save referee instructions
		games_query_set = Game.objects.filter(status__exact= settings.GAME_STATUS['Drawn'])

		games_query_set_count = games_query_set.count()

		if games_query_set_count == 0:
			raise CustomApiException("Game not found", status.HTTP_404_NOT_FOUND)

		inprogress_game_query_set = Game.objects.filter(status__exact= settings.GAME_STATUS['InProgress'])

		if inprogress_game_query_set.count() > 0:
			raise CustomApiException("Please complete the game in progress", status.HTTP_400_BAD_REQUEST)

		current_game = games_query_set[0]
		if current_game.id != game_id:
			raise CustomApiException("Please toss for Game id {0}".format(str(current_game.id)), status.HTTP_400_BAD_REQUEST)

		if randint(1,2) == 1:
			current_game.player_one.role = settings.PLAYER_ROLE['Offensive']
			current_game.player_two.role = settings.PLAYER_ROLE['Defensive']
		else:
			current_game.player_one.role = settings.PLAYER_ROLE['Defensive']
			current_game.player_two.role = settings.PLAYER_ROLE['Offensive']

		
		current_game.player_one.status = settings.PLAYER_STATUS['Playing']
		current_game.player_two.status = settings.PLAYER_STATUS['Playing']

		current_game.player_one.save()
		current_game.player_two.save()

		current_game.status = settings.GAME_STATUS['InProgress']

		current_game.save()

		#send notification and next_instruction to referee
		notification = settings.TOSS_NOTIFICATION.format(current_game.player_one.name, current_game.player_one.role,
			current_game.player_two.name, current_game.player_two.role)
		instruction = settings.TOSS_INSTRUCTION

		self.referee_instruction(current_game.championship,current_game,current_game.player_one, current_game.player_two, 
			notification, instruction)

		referee = Referee.objects.latest('date_created')

		return referee


















