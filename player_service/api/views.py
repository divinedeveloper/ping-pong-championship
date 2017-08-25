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
from api.services import Services 
from api.serializers import PlayerSerializer, ChampionshipSerializer, GameSerializer, RefereeSerializer, PlayerTokenSerializer

# Create your views here.

@csrf_exempt
def login(request):
	"""
	Login with player name

	returns: 
	token
	"""
	try:
		pay_load = json.loads(request.body)

		if pay_load['name'] is None or pay_load['name'] == "":
			raise CustomApiException("Please login using player name", status.HTTP_400_BAD_REQUEST)

		service = Services()
		player_token = service.login(pay_load['name'])

		player_token_serializer = PlayerTokenSerializer(player_token)

		HttpResponse.status_code = status.HTTP_200_OK
		return JsonResponse({'message': "Logged in as {0}. Draw toss for Game".format(pay_load['name']), 
			"player_token": player_token_serializer.data})
	except CustomApiException as err:
		HttpResponse.status_code = err.status_code
		return JsonResponse({'status_code': err.status_code, 'message': err.detail})
	except Exception, e:
		HttpResponse.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return JsonResponse({'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': str(e)})



@csrf_exempt
def offensive_move(request):
	try:
		pay_load = json.loads(request.body)

		if not pay_load['move']:
			raise CustomApiException("Please provide a random number from 1 to 10", status.HTTP_400_BAD_REQUEST)

		if pay_load['move'] == 0 or not(isinstance(pay_load['move'], int)) or (pay_load['move'] not in range(1,11)):
			raise CustomApiException("Please provide a random number from 1 to 10 only", status.HTTP_400_BAD_REQUEST)

		service = Services()
		referee_response = service.offensive_move(pay_load['move'])

		referee_serializer = RefereeSerializer(referee_response)

		HttpResponse.status_code = status.HTTP_200_OK
		return JsonResponse({'message': referee_serializer.data['notification'] + referee_serializer.data['next_instruction'], 
			"referee": referee_serializer.data})
	except CustomApiException as err:
		HttpResponse.status_code = err.status_code
		return JsonResponse({'status_code': err.status_code, 'message': err.detail})
	except Exception, e:
		HttpResponse.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return JsonResponse({'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': str(e)})

@csrf_exempt
def defensive_move(request):
	try:
		pay_load = json.loads(request.body)

		if not pay_load['move']:
			raise CustomApiException("Please provide defense array of random numbers (from 1 to 10)", status.HTTP_400_BAD_REQUEST)

		if not all(isinstance(item, int) for item in pay_load['move']):
			raise CustomApiException("Please provide defense array of Numbers only", status.HTTP_400_BAD_REQUEST)

		service = Services()
		referee_response = service.defensive_move(pay_load['move'])

		referee_serializer = RefereeSerializer(referee_response)

		HttpResponse.status_code = status.HTTP_200_OK
		return JsonResponse({'message': referee_serializer.data['notification'] + referee_serializer.data['next_instruction'], 
			"referee": referee_serializer.data})
	except CustomApiException as err:
		HttpResponse.status_code = err.status_code
		return JsonResponse({'status_code': err.status_code, 'message': err.detail})
	except Exception, e:
		HttpResponse.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return JsonResponse({'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': str(e)})

