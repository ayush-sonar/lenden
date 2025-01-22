from rest_framework import serializers
from .models import Game, Move
from django.contrib.auth import get_user_model

User = get_user_model()

class MoveSerializer(serializers.ModelSerializer):
    player = serializers.CharField(source='player.username', read_only=True)

    class Meta:
        model = Move
        fields = ('id', 'player', 'player_username', 'pos_x', 'pos_y', 
                 'timestamp', 'move_number')
        read_only_fields = ('player', 'move_number')

class GameSerializer(serializers.ModelSerializer):
    p1_username = serializers.CharField(source='p1.username', read_only=True)
    p2_username = serializers.CharField(source='p2.username', read_only=True)
    currentTurn_username = serializers.CharField(source='currentTurn.username', read_only=True)
    winner_username = serializers.CharField(source='winner.username', read_only=True)
    moves = MoveSerializer(many=True, read_only=True)
    
    class Meta:
        model = Game
        fields = ('id', 'p1', 'p2', 'p1_username', 'p2_username',
                 'currentTurn', 'currentTurn_username', 'status', 'winner', 
                 'winner_username', 'canvas', 'created_at', 'updated_at', 'moves')
        read_only_fields = ('canvas', 'winner', 'current_turn')


