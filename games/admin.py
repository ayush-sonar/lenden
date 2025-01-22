from django.contrib import admin
from .models import Game, Move

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'p1', 'p2', 'status', 'winner', 'created_at')
    list_filter = ('status',)
    search_fields = ('p1__username', 'p2__username')

@admin.register(Move)
class MoveAdmin(admin.ModelAdmin):
    list_display = ('game', 'player', 'pos_x', 'pos_y', 'move_number')
    list_filter = ('game',)