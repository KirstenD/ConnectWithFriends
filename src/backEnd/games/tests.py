from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APITestCase

from games.models import Game, Column, Slot


class GameModelTests(TestCase):

    def setUp(self):
        self.alice = User.objects.create_user("alice", "", "password")
        self.bob = User.objects.create_user("bob", "", "password")

    def test_create_game(self):
        game = Game.create_game(self.alice)
        self.assertEquals(game.player1, self.alice)
        self.assertEquals(game.player2, None)
        self.assertEquals(Column.objects.filter(game=game).count(), 7)
        for col in Column.objects.filter(game=game):
            self.assertEquals(Slot.objects.filter(column=col).count(), 6)

    def test_print_empty_board(self):
        assert True

    def test_print_non_empty_board(self):
        assert True

    def test_win_game_horizontal(self):
        assert True

    def test_win_game_vertical(self):
        assert True

    def test_win_game_diagonal(self):
        assert True

    def test_stalemate(self):
        assert True


class MoveViewTests(APITestCase):

    def test_valid_move(self):
        assert True

    def test_full_column(self):
        assert True

    def test_not_your_turn(self):
        assert True

    def test_game_over(self):
        assert True

    def test_win_game(self):
        assert True

    def test_not_in_a_game(self):
        assert True


class LeaveViewTest(APITestCase):

    def test_leave_game(self):
        assert True

    def test_leave_stalemate(self):
        assert True

    def test_not_in_a_game(self):
        assert True


class DetailViewTest(APITestCase):

    def test_view_board(self):
        assert True

    def test_not_in_a_game(self):
        assert True


class StartViewTest(APITestCase):

    def test_first_player(self):
        assert True

    def test_second_player(self):
        assert True

    def test_already_in_game(self):
        assert True
