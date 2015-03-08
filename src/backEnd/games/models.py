from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from games.exceptions import GameFull, IllegalMove


class Game(models.Model):
    player1 = models.ForeignKey(User, related_name="player1")
    player2 = models.ForeignKey(User, related_name="player2",
                                blank=True, null=True, default=None)
    winner = models.ForeignKey(User, related_name="winner",
                               blank=True, null=True, default=None)
    turn = models.ForeignKey(User, related_name="turn",
                             blank=True, null=True, default=None)
    stalemate = models.BooleanField(default=False)
    column_count = 7
    row_count = 6

    @classmethod
    def create_game(cls, player):
        game = Game.objects.create(player1=player)
        for i in range(cls.column_count):
            col = Column.objects.create(index=i, game=game)
            for j in range(cls.row_count):
                Slot.objects.create(index=j, column=col)
        return game

    @classmethod
    def join_or_create(cls, player):
        """
        Join a game if there is one available or create one.

        Leaves any games the player is currently in.
        """
        current_game = Game.active_game(player)
        if current_game:
            current_game.leave(player)
        available_games = Game.objects.filter(player2=None)
        if available_games.count():
            try:
                available_games[0].join(player)
                return available_games[0]
            except GameFull:
                pass
        return cls.create_game(player)

    @classmethod
    def get_games(cls, player):
        """
        Get all games containing a specified player.
        """
        games_as_player1 = cls.objects.filter(player1=player) 
        games_as_player2 = cls.objects.filter(player2=player)
        return games_as_player1 | games_as_player2

    @classmethod
    def active_game(cls, player):
        """
        Return active game player is in or None if the player is not in an
        active game.
        """
        games = Game.get_games(player).order_by("-pk")
        if not games:
            return None
        return games[0]

    def leave(self, player):
        if not self.stalemate and not self.winner:
            assert player == self.player1 or player == self.player2
            if self.player1 == player:
                self.winner = self.player2
            else:
                self.winner = self.player2
            self.turn = None
            self.save()

    def get_board(self):
        columns = Column.objects.filter(game=self).order_by("index")
        board = [[None] * Game.column_count for _ in range(Game.row_count)]
        for column in columns:
            for slot in Slot.objects.filter(column=column).order_by("index"):
                board[slot.index][column.index] = slot.player
        return board

    def move(self, player, index):
        """
        :arg player: Player making the move
        :type player: User
        :arg index: Index of column to place a token in
        :type index: Int
        """
        if self.turn != player:
            raise IllegalMove("It is not your turn.")
        try:
            column = Column.objects.get(game=self, index=index)
        except ObjectDoesNotExist:
            raise IllegalMove("No such column.")
        slots = Slot.objects.filter(column=column).order_by("index")
        if slots[0].player is not None:
            raise IllegalMove("Cannot place token in full column")
        i = 0
        while i < Game.row_count and slots[i].player is None:
            i += 1
        slot = slots[i - 1]
        slot.player = player
        slot.save()
        if player == self.player1:
            self.turn = self.player2
        else:
            self.turn = self.player1
        self._check_board()

    def join(self, player):
        """
        Join a game that is missing a player.
        """
        if self.player2 is not None:
            raise GameFull("There are already 2 players in this game.")
        self.player2 = player
        self.turn = self.player1
        self.save()

    def _check_board(self):
        """
        Checks the board for a winner or stalemate and updates the game state.
        """
        winner = self._check_winner()
        if winner:
            self.winner = winner
        else:
            if self._board_is_full():
                self.stalemate = True
                self.turn = None
        self.save()

    def _board_is_full(self):
        """
        Returns True if every slot in the board is occupied.
        """
        for column in self.get_board():
            for player in column:
                if not player:
                    return False
        return True

    def _check_winner_in_sequence(self, sequence):
        """
        Determine if there is a sequence of 4 tokens from the same player in a
        list.
        """
        current_streak = 0
        current_player = None
        for token in sequence:
            if token is not None and token == current_player:
                current_streak += 1
                if current_streak >= 4:
                    return current_player
            else:
                current_streak = 1
                current_player = token

    def _check_winner(self):
        """
        Return the winning player if there is one, else return None.
        """
        board = self.get_board()

        # Horizontal winning conditions
        for row in board:
            winner = self._check_winner_in_sequence(row)
            if winner:
                return winner

        # Vertical winning conditions
        for col_index in range(Game.column_count):
            sequence = []
            for row_index in range(Game.row_count):
                sequence.append(board[row_index][col_index])
            winner = self._check_winner_in_sequence(sequence)
            if winner:
                return winner

        # Diagonal down-right winning conditions
        for col_index in range(Game.column_count - 3):
            row_index = 0
            sequence = []
            while col_index < Game.column_count and row_index < Game.row_count:
                sequence.append(board[row_index][col_index])
                row_index += 1
                col_index += 1
            winner = self._check_winner_in_sequence(sequence)
            if winner:
                return winner

        for row_index in range(Game.row_count - 3):
            col_index = 0
            sequence = []
            while col_index < Game.column_count and row_index < Game.row_count:
                sequence.append(board[row_index][col_index])
                row_index += 1
                col_index += 1
            winner = self._check_winner_in_sequence(sequence)
            if winner:
                return winner

        # Diagonal down-left winning conditions
        for col_index in range(3, Game.column_count):
            row_index = 0
            sequence = []
            while col_index >= 0 and row_index < Game.row_count:
                sequence.append(board[row_index][col_index])
                row_index += 1
                col_index -= 1
            winner = self._check_winner_in_sequence(sequence)
            if winner:
                return winner

        for row_index in range(Game.row_count - 3):
            col_index = 6
            sequence = []
            while col_index >= 0 and row_index < Game.row_count:
                sequence.append(board[row_index][col_index])
                row_index += 1
                col_index -= 1
            winner = self._check_winner_in_sequence(sequence)
            if winner:
                return winner

    def __unicode__(self):
        board = self.get_board()
        return "\n".join(str(row) for row in board)


class Column(models.Model):
    game = models.ForeignKey(Game)
    index = models.IntegerField()

    def __unicode__(self):
        return str(self.index)


class Slot(models.Model):
    column = models.ForeignKey(Column)
    index = models.IntegerField()
    player = models.ForeignKey(User, blank=True, null=True)

    def __unicode__(self):
        return str(self.player)
