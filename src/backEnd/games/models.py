from django.contrib.auth.models import User
from django.db import models

from games.exceptions import GameFull


class Game(models.Model):
    active_player = models.ForeignKey(User,
                                      related_name="active_player",
                                      blank=True,
                                      default=None)
    winner = models.ForeignKey(User,
                               related_name="winner",
                               blank=True,
                               default=None)
    stalemate = models.BooleanField(default=False)
    player1 = models.ForeignKey(User, related_name="player1")
    player2 = models.ForeignKey(User,
                                related_name="player2",
                                blank=True,
                                default=None)
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
    def get_games(cls, player):
        """
        Get all games containing a specified player.
        """
        return cls.objects.filter(player1=player) | cls.objects.filter(player2=player)

    def get_board(self):
        columns = Column.objects.filter(game=self).order_by("index")
        board = []
        for column in columns:
            slots = Slot.objects.filter(column=column).order_by("index")
            board.append([slot for slot in slots])
        return board

    def is_active(self):
        if self.winner or self.stalemate:
            return True
        return False

    def move(self, player, column):
        """
        :arg player: Player making the move
        :type player: User
        :arg column: Index of column to place a token in
        :type column: Int
        """
        pass

    def join(self, player):
        """
        Join a game that is missing a player.
        """
        if self.player2:
            raise GameFull("There are already 2 players in this game.")
        self.player2 = player
        self.active_player = self.player1


class Column(models.Model):
    game = models.ForeignKey(Game)
    index = models.IntegerField()

    def __unicode__(self):
        return str(self.index)


class Slot(models.Model):
    column = models.ForeignKey(Column)
    index = models.IntegerField()
    player = models.ForeignKey(User, blank=True)

    def __unicode__(self):
        return str(self.player)
