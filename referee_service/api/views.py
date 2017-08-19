# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
from django.shortcuts import render
from random import randint, sample
from django.conf import settings
import requests
import json

# Create your views here.

game_report = []


def player_registration():
	"""
	Initial player registration and set his status as active.

	Iterate on players list and add one more key 'is_active' to all players
	Transfers call to draw initial games for players
	"""

	try:
		players_list_response = requests.get(settings.GET_PLAYERS_URL)

		players_data_list = players_list_response.json()['players_data_list']
	except requests.exceptions.RequestException as e:
		print "ERROR: Failed to connect with Player service. Please check if it is running."
		print e
		sys.exit(1)

	print "#" * 10 + " Player Registration Starts " + "#" * 10

	for players_data in players_data_list:
		#call the participate function to join each player in game
		players_data['is_active'] = True
		print players_data['player_name'] + ' joined the game'


	print "#" * 10 + " Player Registration Ends " + "#" * 10

	draw_games(players_data_list)

def draw_games(players_data_list):
	"""
	Referee Draw Games for random players and notifies them.
	"""
	try:

		players_match_list = []

		while len(players_data_list) >= 2:
			player_one = players_data_list.pop(randint(0, len(players_data_list)-1 ))
			player_two = players_data_list.pop(randint(0, len(players_data_list)-1 ))

			players_match_list.append((player_one, player_two))

		for index, each_match in enumerate(players_match_list):
			print "Game id  " + str(index+1)
			print "player 1 " + each_match[0]['player_name'] + " offensive player"
			print "player 2 " + each_match[1]['player_name']
			print "--"*10

		start_matches(players_match_list, players_data_list)
	except Exception as e: print(e) 


def start_matches(players_match_list, players_data_list):
	"""
	Start matches between players one at a time.

	Declares match winner, shuts down lost players
	After final game call export report
	"""
	match_winners_list = []
	match_loosers_list = []

	if len(players_match_list) >= 1:
		for index in xrange(0, len(players_match_list)):
			match_players_tuple = players_match_list.pop(0)
			match_player_one = match_players_tuple[0]
			match_player_two = match_players_tuple[1]

			#call the function to play game and return winner
			#append winner to match winners list
			print "#"*10 + "Start Game No. " + str(index+1) + "#"*10

			match_winner, match_looser = play_match(match_player_one, match_player_two)
			match_winners_list.append(match_winner)
			match_loosers_list.append(match_looser)

			print "Match Winner is " + match_winner['player_name']

			print "#"*10 + "End Game No. " + str(index+1) + "#"*10

		#shutdown defeated players by setting them inactive
		for lost_player in match_loosers_list:
			try:
				players_response = requests.post(settings.PLAYER_SHUTDOWN_URL, data= lost_player)
				print lost_player['player_name'] + " got shutdown"
			except requests.exceptions.RequestException as e:
				print "ERROR: Failed to connect with Player service. Please check if it is running."
				print e
				sys.exit(1)
				

		if len(match_winners_list) > 1:
			draw_games(match_winners_list)

	if len(match_winners_list) == 1:
		print "\t"*5 + "*"*10 + "Ping Pong Champion Cup Winner is " + match_winners_list[0]['player_name'] + "*"*10 + "\n"
		export_report()
		return

def play_match(match_player_one, match_player_two):
	"""
	Each player plays moves depending on his type.

	Move winner is decided and finally one whos reaches game wining points first 
	is declared winner
	"""

	player_one_points = 0
	player_two_points = 0
	player_one_type = "offensive"
	player_two_type = "defensive" 
	match_winner = None
	match_looser = None

	while(player_one_points < settings.GAME_WINNING_POINTS and player_two_points < settings.GAME_WINNING_POINTS):
		player_one_move = get_player_move(match_player_one, player_one_type)
		player_two_move = get_player_move(match_player_two, player_two_type)
		player_one_type, player_one_points, player_two_type, player_two_points = judge_move_winner_and_player_type(player_one_type, 
			player_one_move, player_one_points,	player_two_type, player_two_move, player_two_points)

	if player_one_points > player_two_points:
		match_winner = match_player_one
		match_looser = match_player_two
	else:
		match_winner = match_player_two
		match_looser = match_player_one

	#IMP add match report
	game_report.append({
		'players': [match_player_one['player_name'], match_player_two['player_name']],
		'points': [player_one_points, player_two_points],
		'winner': match_winner['player_name']
		})
	return (match_winner, match_looser)


def get_player_move(match_player, player_type):
	"""
	Make REST API call to player service to get moves based on their type.

	"""
	try:
		payload = {'player_type': player_type, 'player_defence_set_length': match_player['player_defence_set_length']}
		player_move_response = requests.get(settings.GET_PLAYER_MOVES_URL, params=payload)

		return player_move_response.json()['player_move']
	except requests.exceptions.RequestException as e:
		print "ERROR: Failed to connect with Player service. Please check if it is running."
		print e
		sys.exit(1)


def judge_move_winner_and_player_type(player_one_type, player_one_move, player_one_points, player_two_type, player_two_move, player_two_points):
	"""
	Based on player type, Check his move in opponents array.

	Increase winners points and set type of players
	"""

	if player_one_type == "offensive":
		if player_one_move not in player_two_move:
			#increment point of player one
			# one type will be offensive
			#two type will be defensive
			player_one_points += 1
			player_one_type = "offensive"
			player_two_type = "defensive"
		else:
			#increment point of player TWO
			# two type will be offensive
			#one type will be defensive
			player_two_points += 1
			player_two_type = "offensive"
			player_one_type = "defensive"
	else:
		if player_two_move not in player_one_move:
			#increment point of player two
			# two type will be offensive
			#one type will be defensive
			player_two_points += 1
			player_two_type = "offensive"
			player_one_type = "defensive"
		else:
			#increment point of player One
			# one type will be offensive
			#two type will be defensive
			player_one_points += 1
			player_one_type = "offensive"
			player_two_type = "defensive"

	return (player_one_type, player_one_points, player_two_type, player_two_points)

def export_report():
	"""
	Prints Final Game report of all matches.
	"""
	print "\t"*5 + "#"*10 + " Game Report "+ "#"*10

	for index, each_game in enumerate(game_report):
		print "\t"*5 + "*"*40
		print "\t"*5 + "Game No - " + str(index+1)
		print "\t"*5 + "Players - " + each_game['players'][0] + " vs " + each_game['players'][1]
		print "\t"*5 + "Scores - " + str(each_game['points'][0]) + " vs " + str(each_game['points'][1])
		print "\t"*5 + "Winner - " + each_game['winner']

	return










