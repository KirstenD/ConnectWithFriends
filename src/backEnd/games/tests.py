from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APITestCase

from games.exceptions import GameFull, IllegalMove
from games.models import Game, Column, Slot


class GameModelTests(TestCase):

    def setUp(self):
        self.alice = User.objects.create_user("alice", "", "password")
        self.bob = User.objects.create_user("bob", "", "password")
        self.casey = User.objects.create_user("casey", "", "password")

    def test_create_game(self):
        game = Game.create_game(self.alice)
        self.assertEquals(game.turn, None)
        self.assertEquals(game.player1, self.alice)
        self.assertEquals(game.player2, None)
        self.assertEquals(Column.objects.filter(game=game).count(), 7)
        for col in Column.objects.filter(game=game):
            self.assertEquals(Slot.objects.filter(column=col).count(), 6)

    def test_join_game(self):
        game = Game.create_game(self.alice)
        game.join(self.bob)
        self.assertEquals(game.turn, self.alice)
        self.assertEquals(game.player1, self.alice)
        self.assertEquals(game.player2, self.bob)

    def test_join_full_game(self):
        game = Game.create_game(self.alice)
        game.join(self.bob)
        self.assertRaises(GameFull, game.join, self.casey)

    def test_stalemate(self):
        """
        BBBABBB
        AAABAAA
        BBBABBB
        AAABAAA
        BBBABBB
        AAABAAA
        """
        game = Game.create_game(self.alice)
        game.join(self.bob)
        for _ in range(3):
            game.move(self.alice, 0)
            game.move(self.bob, 0)
            game.move(self.alice, 1)
            game.move(self.bob, 1)
            game.move(self.alice, 2)
            game.move(self.bob, 2)
            game.move(self.alice, 4)
            game.move(self.bob, 3)
            game.move(self.alice, 3)
            game.move(self.bob, 4)
            game.move(self.alice, 5)
            game.move(self.bob, 5)
            game.move(self.alice, 6)
            game.move(self.bob, 6)
        self.assertEqual(game.stalemate, True)
        self.assertEqual(game.winner, None)

    def test_get_board_empty(self):
        game = Game.create_game(self.alice)
        game.join(self.bob)
        for row in game.get_board():
            for col in row:
                self.assertEquals(col, None)

    def test_get_with_token(self):
        game = Game.create_game(self.alice)
        game.join(self.bob)
        column = Column.objects.get(game=game, index=0)
        slot = Slot.objects.get(column=column, index=5)
        slot.player = self.alice
        slot.save()
        self.assertEquals(game.get_board()[5][0], self.alice)

    def test_move(self):
        game = Game.create_game(self.alice)
        game.join(self.bob)
        game.move(self.alice, 0)
        self.assertEquals(game.get_board()[5][0], self.alice)

    def test_move_stacking_tokens(self):
        game = Game.create_game(self.alice)
        game.join(self.bob)
        game.move(self.alice, 0)
        game.move(self.bob, 0)
        game.move(self.alice, 0)
        board = game.get_board()
        self.assertEquals(board[5][0], self.alice)
        self.assertEquals(board[4][0], self.bob)
        self.assertEquals(board[3][0], self.alice)
        self.assertEquals(game.winner, None)
        self.assertEquals(game.stalemate, False)

    def test_move_one_player(self):
        game = Game.create_game(self.alice)
        self.assertRaises(IllegalMove, game.move, self.alice, 0)

    def test_move_taking_turns(self):
        game = Game.create_game(self.alice)
        game.join(self.bob)
        self.assertEquals(game.turn, self.alice)
        game.move(self.alice, 0)
        self.assertEquals(game.turn, self.bob)
        game.move(self.bob, 1)
        self.assertEquals(game.turn, self.alice)

    def test_move_not_your_turn(self):
        game = Game.create_game(self.alice)
        game.join(self.bob)
        self.assertRaises(IllegalMove, game.move, self.bob, 0)

    def test_move_invalid_player(self):
        game = Game.create_game(self.alice)
        game.join(self.bob)
        self.assertRaises(IllegalMove, game.move, self.casey, 0)

    def test_move_invalid_column(self):
        game = Game.create_game(self.alice)
        game.join(self.bob)
        self.assertRaises(IllegalMove, game.move, self.alice, 7)

    def test_move_full_column(self):
        game = Game.create_game(self.alice)
        game.join(self.bob)
        game.move(self.alice, 0)
        game.move(self.bob, 0)
        game.move(self.alice, 0)
        game.move(self.bob, 0)
        game.move(self.alice, 0)
        game.move(self.bob, 0)
        self.assertRaises(IllegalMove, game.move, self.alice, 0)

    def test_winning_move_horizontal(self):
        game = Game.create_game(self.alice)
        game.join(self.bob)
        game.move(self.alice, 0)
        game.move(self.bob, 0)
        game.move(self.alice, 1)
        game.move(self.bob, 1)
        game.move(self.alice, 2)
        game.move(self.bob, 2)
        game.move(self.alice, 3)
        self.assertEqual(game.winner, self.alice)

    def test_winning_move_vertical(self):
        game = Game.create_game(self.alice)
        game.join(self.bob)
        game.move(self.alice, 2)
        game.move(self.bob, 1)
        game.move(self.alice, 0)
        game.move(self.bob, 1)
        game.move(self.alice, 0)
        game.move(self.bob, 1)
        game.move(self.alice, 0)
        game.move(self.bob, 1)
        self.assertEqual(game.winner, self.bob)

    def test_winning_move_diagonal_upper_left(self):
        """
        000A000
        00AB000
        0AAA000
        ABBB000
        BAAA000
        ABBB00B
        """
        game = Game.create_game(self.alice)
        game.join(self.bob)
        game.move(self.alice, 0)
        game.move(self.bob, 0)
        game.move(self.alice, 0)
        game.move(self.bob, 1)
        game.move(self.alice, 1)
        game.move(self.bob, 1)
        game.move(self.alice, 1)
        game.move(self.bob, 2)
        game.move(self.alice, 2)
        game.move(self.bob, 2)
        game.move(self.alice, 2)
        game.move(self.bob, 6)
        game.move(self.alice, 2)
        game.move(self.bob, 3)
        game.move(self.alice, 3)
        game.move(self.bob, 3)
        game.move(self.alice, 3)
        game.move(self.bob, 3)
        self.assertEqual(game.winner, None)
        game.move(self.alice, 3)
        self.assertEqual(game.winner, self.alice)

    def test_winning_move_diagonal_upper_right(self):
        """
        000A000
        000BA00
        000AAA0
        000BBBA
        000AAAB
        B00BBBA
        """
        game = Game.create_game(self.alice)
        game.join(self.bob)
        game.move(self.alice, 6)
        game.move(self.bob, 6)
        game.move(self.alice, 6)
        game.move(self.bob, 5)
        game.move(self.alice, 5)
        game.move(self.bob, 5)
        game.move(self.alice, 5)
        game.move(self.bob, 4)
        game.move(self.alice, 4)
        game.move(self.bob, 4)
        game.move(self.alice, 4)
        game.move(self.bob, 0)
        game.move(self.alice, 4)
        game.move(self.bob, 3)
        game.move(self.alice, 3)
        game.move(self.bob, 3)
        game.move(self.alice, 3)
        game.move(self.bob, 3)
        self.assertEqual(game.winner, None)
        game.move(self.alice, 3)
        self.assertEqual(game.winner, self.alice)

    def test_winning_move_diagonal_lower_left(self):
        """
        0000000
        0000000
        A000000
        BA00000
        BBA0000
        AABA00B
        """
        game = Game.create_game(self.alice)
        game.join(self.bob)
        game.move(self.alice, 0)
        game.move(self.bob, 0)
        game.move(self.alice, 1)
        game.move(self.bob, 0)
        game.move(self.alice, 0)
        game.move(self.bob, 1)
        game.move(self.alice, 1)
        game.move(self.bob, 2)
        game.move(self.alice, 2)
        game.move(self.bob, 6)
        self.assertEqual(game.winner, None)
        game.move(self.alice, 3)
        self.assertEqual(game.winner, self.alice)

    def test_winning_move_diagonal_lower_right(self):
        """
        0000000
        0000000
        000000A
        00000AB
        0000ABB
        B00ABAA
        """
        game = Game.create_game(self.alice)
        game.join(self.bob)
        game.move(self.alice, 6)
        game.move(self.bob, 6)
        game.move(self.alice, 5)
        game.move(self.bob, 6)
        game.move(self.alice, 6)
        game.move(self.bob, 5)
        game.move(self.alice, 5)
        game.move(self.bob, 4)
        game.move(self.alice, 4)
        game.move(self.bob, 0)
        self.assertEqual(game.winner, None)
        game.move(self.alice, 3)
        self.assertEqual(game.winner, self.alice)


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
