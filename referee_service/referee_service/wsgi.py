"""
WSGI config for referee_service project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "referee_service.settings")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

players_data_file =  os.path.join(BASE_DIR, 'players_data.json')

with open(players_data_file) as json_file:
	players_data_list = data1 = json.load(json_file)

for players_data in players_data_list:
	#call the participate function to join each player in game
	print players_data['player_name'] + 'joined the game'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
