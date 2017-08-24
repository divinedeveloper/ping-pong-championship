from rest_framework import serializers
from api.models import Player, Championship, Game, PlayerToken, Referee

class PlayerSerializer(serializers.ModelSerializer):
	"""
	Player serializer for player records
	depth field automatically serializes all fields in nested relations to. 
	"""
	class Meta:
		model = Player
		fields = '__all__'
		depth = 3

class ChampionshipSerializer(serializers.ModelSerializer):
	"""
	Championship serializer for tournament
	depth field automatically serializes all fields in nested relations to. 
	"""
	class Meta:
		model = Championship
		fields = '__all__'
		depth = 3

class GameSerializer(serializers.ModelSerializer):
	"""
	Game serializer for tournament
	depth field automatically serializes all fields in nested relations to. 
	"""
	class Meta:
		model = Game
		fields = '__all__'
		depth = 3


class RefereeSerializer(serializers.ModelSerializer):
	"""
	Referee serializer for tournament
	depth field automatically serializes all fields in nested relations to. 
	"""
	class Meta:
		model = Referee
		fields = '__all__'
		depth = 3

class PlayerTokenSerializer(serializers.ModelSerializer):
	"""
	PlayerToken serializer for tournament
	depth field automatically serializes all fields in nested relations to. 
	"""
	class Meta:
		model = PlayerToken
		fields = '__all__'
		depth = 3