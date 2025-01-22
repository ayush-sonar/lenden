from games.models import Move

class Logic:
    def __init__(self, game):
        self.game = game

    def activate_game(self):
        if self.game.status != 'P':
            raise ValueError("Game is not in pending state")
        
        # Initialize the game board
        self.game.canvas = {
            "canvas": [[None, None, None],
                      [None, None, None],
                      [None, None, None]],
            "current_symbol": "X"
        }
        
        self.game.status = 'A'
        self.game.save()
        return self.game

    def make_move(self, player, x, y):
        # Status should be 'A' (Active) not 'P' (Pending) for ongoing games
        if self.game.status != 'A':
            raise ValueError("Game is not in progress")
        
        if self.game.currentTurn != player:
            raise ValueError("Not your turn")
        
        if not (0 <= x <= 2 and 0 <= y <= 2):
            raise ValueError("Invalid position")

        canvas = self.game.canvas['canvas']
        if canvas[x][y] is not None:
            raise ValueError("Position already taken")

        # Make the move
        symbol = self.game.canvas['current_symbol']
        canvas[x][y] = symbol

        # Create move record - Fixed the move count
        move_number = Move.objects.filter(game=self.game).count() + 1
        Move.objects.create(
            game=self.game,
            player=player,
            pos_x=x,
            pos_y=y,
            move_number=move_number
        )

        # Check for win
        if self._check_win(canvas, symbol):
            self.game.status = 'F'
            self.game.winner = player
            self._update_stats(player, 'win')
        # Check for draw
        elif self._is_canvas_full(canvas):
            self.game.status = 'F'
            self._update_stats(player, 'draw')
        else:
            # Switch turns
            self.game.currentTurn = (
                self.game.p2 
                if player == self.game.p1 
                else self.game.p1
            )
            self.game.canvas['current_symbol'] = 'O' if symbol == 'X' else 'X'

        self.game.canvas['canvas'] = canvas
        self.game.save()
        return self.game

    def _check_win(self, canvas, symbol):
        # Check rows
        for row in canvas:
            if all(cell == symbol for cell in row):
                return True

        # Check columns
        for col in range(3):
            if all(canvas[row][col] == symbol for row in range(3)):
                return True

        # Check diagonals
        if all(canvas[i][i] == symbol for i in range(3)):
            return True
        if all(canvas[i][2-i] == symbol for i in range(3)):
            return True

        return False

    def _is_canvas_full(self, canvas):
        return all(cell is not None for row in canvas for cell in row)

    def _update_stats(self, player, result):
        player.games_played += 1
        other_player = (
            self.game.p2 
            if player == self.game.p1 
            else self.game.p1
        )
        other_player.games_played += 1

        if result == 'win':
            player.games_won += 1
            other_player.games_lost += 1
        elif result == 'draw':
            player.games_drawn += 1
            other_player.games_drawn += 1

        player.save()
        other_player.save()