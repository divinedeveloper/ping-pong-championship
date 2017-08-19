# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import json
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework import status
from api.custom_exceptions import CustomApiException
from random import randint, sample

# Create your views here.

@csrf_exempt
def get_players(request):
	"""
	Request ask for players list to register.

	returns: 
	List of players
	"""
	try:
		BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

		players_data_file =  os.path.join(BASE_DIR, 'players_data.json')

		with open(players_data_file) as json_file:
			players_data_list = json.load(json_file)


		HttpResponse.status_code = status.HTTP_200_OK
		return JsonResponse({"players_data_list": players_data_list})
	except CustomApiException as err:
		HttpResponse.status_code = err.status_code
		return JsonResponse({'status_code': err.status_code, 'message': err.detail})
	except Exception, e:
		HttpResponse.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return JsonResponse({'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': str(e)})

@csrf_exempt
def get_player_move(request):
	"""
	Request contains player type(offensive/defensive) and defence set length(eg. 5).

	returns: 
	random int number from 1-10 if offensive
	list of random numbers if defensive
	"""
	try:
		player_type = request.GET.get('player_type', '')
		player_defence_set_length = request.GET.get('player_defence_set_length', '')

		if player_type == "" or player_type == None:
			raise CustomApiException("Please provide player type", status.HTTP_400_BAD_REQUEST)

		if player_defence_set_length == "" or player_defence_set_length == None or int(player_defence_set_length) == 0:
			raise CustomApiException("Please provide player's defence set length", status.HTTP_400_BAD_REQUEST)

		if player_type == "offensive":
			player_move = randint(1,10)
		else:
			#generate a list of no.s for 1 to defence length
			player_move = sample(range(1,10), int(player_defence_set_length))

		HttpResponse.status_code = status.HTTP_200_OK
		return JsonResponse({"player_move": player_move})
	except CustomApiException as err:
		HttpResponse.status_code = err.status_code
		return JsonResponse({'status_code': err.status_code, 'message': err.detail})
	except Exception, e:
		HttpResponse.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return JsonResponse({'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': str(e)})

@csrf_exempt
def deactivate_player(request):
	"""
	Request body contains players dict.

	set is_active to false
	returns: player dict
	"""
	try:
		if not request.body:
			raise CustomApiException("Please provide player data", status.HTTP_400_BAD_REQUEST )
		
		if not 'application/json' in request.META.get('CONTENT_TYPE'):
			raise CustomApiException("Please provide request body as json format only", status.HTTP_400_BAD_REQUEST ) 

		json_body = json.loads(request.body)

		for key, value in json_body.iteritems():
			if value is None or value == "":
				raise CustomApiException("Please provide " + key, status.HTTP_400_BAD_REQUEST)

		json_body['is_active'] = False

		HttpResponse.status_code = status.HTTP_200_OK
		return JsonResponse(json_body, safe=False)
	except CustomApiException as err:
		HttpResponse.status_code = err.status_code
		return JsonResponse({'status_code': err.status_code, 'message': err.detail})
	except Exception, e:
		HttpResponse.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return JsonResponse({'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': str(e)})