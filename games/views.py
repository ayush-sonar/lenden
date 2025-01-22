from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import models
from .models import Game, Move
from .serializers import GameSerializer, MoveSerializer , GameDetailSerializer
import random
from .logic import Logic
from users.models import User

class GameViewSet(viewsets.ModelViewSet):
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Game.objects.filter(
            models.Q(p1=self.request.user) | 
            models.Q(p2=self.request.user)
        )

    def create(self, request):
        print(request.data)
        print("test",request.user)
        # Initialize new game
        # print("hehe",request.data.get('p1')
        p1_username = request.data.get('p1')
        p2_username = request.data.get('p2')

        if not p1_username or not p2_username:
            return Response(
                {"error": "Both player usernames are required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            p1 = User.objects.get(username=p1_username)
            p2 = User.objects.get(username=p2_username)
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid player"}, 
                status=status.HTTP_400_BAD_REQUEST
            )


        if not p1:
            return Response(
                {"error": "Player 1 is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        if not p2:
            return Response(
                {"error": "Player 2 is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Randomly decide who goes first
        players = [p1, p2]
        random.shuffle(players)
        first_player = players[0]
        game = Game.objects.create(
            p1=p1,
            p2=p2,
            currentTurn=first_player,
            canvas={
                "canvas": [[None] * 3 for _ in range(3)],
                "current_symbol": "X"
            }
        )
        return Response(
            GameSerializer(game).data, 
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        game = self.get_object()
        
        # Verify this is player2 accepting the game
        if request.user != game.p2:
            return Response(
                {"error": "Only player 2 can accept this game"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            game_logic = Logic(game)
            game = game_logic.activate_game()
            return Response(GameSerializer(game).data)
        except ValueError as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def move(self, request, pk=None):
        game = self.get_object()

        if game.status == 'F':
            return Response(
                {"error": "Game is already finished the winner is " + game.winner.username}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate it's the player's turn
        if game.currentTurn != request.user:
            return Response(
                {"error": "Not your turn"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get move coordinates
        try:
            x = int(request.data.get('pos_x'))
            y = int(request.data.get('pos_y'))
        except (TypeError, ValueError):
            return Response(
                {"error": "Invalid position coordinates"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Make move (we'll implement this method later)
        try:
            logic = Logic(game)
            game = logic.make_move(request.user, x, y)
            return Response(GameSerializer(game).data)
        except ValueError as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class GameHistoryView(generics.ListAPIView):
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print(self.request.user)
        return Game.objects.filter(
            models.Q(p1=self.request.user) | 
            models.Q(p2=self.request.user),
            status='F'
        ).order_by('-created_at')

class GameHistoryDetailView(generics.RetrieveAPIView):
    serializer_class = GameDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Game.objects.filter(
            models.Q(p1=self.request.user) | 
            models.Q(p2=self.request.user),
            status='F'
        )