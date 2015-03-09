from django.core.urlresolvers import reverse
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
        game = Game._create_game(self.alice)
        self.assertEquals(game.turn, None)
        self.assertEquals(game.player1, self.alice)
        self.assertEquals(game.player2, None)
        self.assertEquals(game.winner, None)
        self.assertEquals(Column.objects.filter(game=game).count(), Game.column_count)
        for col in Column.objects.filter(game=game):
            self.assertEquals(Slot.objects.filter(column=col).count(), Game.row_count)

    def test_create_game_already_in_game(self):
        first_game = Game._create_game(self.alice)
        second_game = Game._create_game(self.alice)
        self.assertEquals(first_game.turn, None)
        self.assertEquals(first_game.player1, self.alice)
        self.assertEquals(first_game.player2, None)
        self.assertEquals(first_game.winner, None)
        self.assertEquals(Game.current_game(self.alice), second_game)
        self.assertEquals(second_game.turn, None)
        self.assertEquals(second_game.player1, self.alice)
        self.assertEquals(second_game.player2, None)
        self.assertEquals(second_game.winner, None)

    def test_join_game(self): 
        game = Game._create_game(self.alice)
        game.join(self.bob)
        self.assertEquals(game.turn, self.alice)
        self.assertEquals(game.player1, self.alice)
        self.assertEquals(game.player2, self.bob)

    def test_new_game_twice(self):
        Game.new_game(self.alice)
        game = Game.new_game(self.alice)
        self.assertEquals(game.turn, None)
        self.assertEquals(game.player1, self.alice)
        self.assertEquals(game.player2, None)

    def test_join_full_game(self):
        game = Game._create_game(self.alice)
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
        game = Game._create_game(self.alice)
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
        game = Game._create_game(self.alice)
        game.join(self.bob)
        for row in game.get_board():
            for col in row:
                self.assertEquals(col, None)

    def test_get_with_token(self):
        game = Game._create_game(self.alice)
        game.join(self.bob)
        column = Column.objects.get(game=game, index=0)
        slot = Slot.objects.get(column=column, index=Game.row_count - 1)
        slot.player = self.alice
        slot.save()
        self.assertEquals(game.get_board()[Game.row_count - 1][0], self.alice)

    def test_move(self):
        game = Game._create_game(self.alice)
        game.join(self.bob)
        game.move(self.alice, 0)
        self.assertEquals(game.get_board()[Game.row_count - 1][0], self.alice)

    def test_move_stacking_tokens(self):
        game = Game._create_game(self.alice)
        game.join(self.bob)
        game.move(self.alice, 0)
        game.move(self.bob, 0)
        game.move(self.alice, 0)
        board = game.get_board()
        self.assertEquals(board[Game.row_count - 1][0], self.alice)
        self.assertEquals(board[4][0], self.bob)
        self.assertEquals(board[3][0], self.alice)
        self.assertEquals(game.winner, None)
        self.assertEquals(game.stalemate, False)

    def test_move_one_player(self):
        game = Game._create_game(self.alice)
        self.assertRaises(IllegalMove, game.move, self.alice, 0)

    def test_move_taking_turns(self):
        game = Game._create_game(self.alice)
        game.join(self.bob)
        self.assertEquals(game.turn, self.alice)
        game.move(self.alice, 0)
        self.assertEquals(game.turn, self.bob)
        game.move(self.bob, 1)
        self.assertEquals(game.turn, self.alice)

    def test_move_not_your_turn(self):
        game = Game._create_game(self.alice)
        game.join(self.bob)
        self.assertRaises(IllegalMove, game.move, self.bob, 0)

    def test_move_invalid_player(self):
        game = Game._create_game(self.alice)
        game.join(self.bob)
        self.assertRaises(IllegalMove, game.move, self.casey, 0)

    def test_move_invalid_column(self):
        game = Game._create_game(self.alice)
        game.join(self.bob)
        self.assertRaises(IllegalMove, game.move, self.alice, 7)

    def test_move_full_column(self):
        game = Game._create_game(self.alice)
        game.join(self.bob)
        game.move(self.alice, 0)
        game.move(self.bob, 0)
        game.move(self.alice, 0)
        game.move(self.bob, 0)
        game.move(self.alice, 0)
        game.move(self.bob, 0)
        self.assertRaises(IllegalMove, game.move, self.alice, 0)

    def test_winning_move_horizontal(self):
        game = Game._create_game(self.alice)
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
        game = Game._create_game(self.alice)
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
        game = Game._create_game(self.alice)
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
        game = Game._create_game(self.alice)
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
        game = Game._create_game(self.alice)
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
        game = Game._create_game(self.alice)
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

    def setUp(self):
        self.alice = User.objects.create_user("alice", "", "password")
        self.bob = User.objects.create_user("bob", "", "password")

    def test_valid_move(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.alice.auth_token))
        self.client.post(reverse("games:start"))
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.bob.auth_token))
        self.client.post(reverse("games:start"))
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.alice.auth_token))
        response = self.client.post(reverse("games:move", args=(0, )))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data["turn"], self.bob.pk)
        self.assertEquals(response.data["board"][Game.row_count - 1][0], self.alice.pk)


    def test_full_column(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.alice.auth_token))
        self.client.post(reverse("games:start"))
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.bob.auth_token))
        self.client.post(reverse("games:start"))
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.alice.auth_token))
        self.client.post(reverse("games:move", args=(0, )))
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.bob.auth_token))
        self.client.post(reverse("games:move", args=(0, )))
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.alice.auth_token))
        self.client.post(reverse("games:move", args=(0, )))
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.bob.auth_token))
        self.client.post(reverse("games:move", args=(0, )))
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.alice.auth_token))
        self.client.post(reverse("games:move", args=(0, )))
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.bob.auth_token))
        self.client.post(reverse("games:move", args=(0, )))
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.alice.auth_token))
        response = self.client.post(reverse("games:move", args=(0, )))
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.data, {"detail": "Cannot place token in full column."})

    def test_not_your_turn(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.alice.auth_token))
        self.client.post(reverse("games:start"))
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.bob.auth_token))
        self.client.post(reverse("games:start"))
        response = self.client.post(reverse("games:move", args=(0, )))
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.data, {"detail": "It is not your turn."})

    def test_game_over(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.alice.auth_token))
        self.client.post(reverse("games:start"))
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.bob.auth_token))
        self.client.post(reverse("games:start"))
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.alice.auth_token))
        self.client.post(reverse("games:move", args=(0, )))
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.bob.auth_token))
        self.client.post(reverse("games:move", args=(0, )))
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.alice.auth_token))
        self.client.post(reverse("games:move", args=(1, )))
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.bob.auth_token))
        self.client.post(reverse("games:move", args=(1, )))
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.alice.auth_token))
        self.client.post(reverse("games:move", args=(2, )))
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.bob.auth_token))
        self.client.post(reverse("games:move", args=(2, )))
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.alice.auth_token))
        response = self.client.post(reverse("games:move", args=(3, )))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data["winner"], self.alice.pk)
        self.assertEquals(response.data["turn"], None)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.bob.auth_token))
        response = self.client.post(reverse("games:move", args=(0, )))
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.data, {"detail": "It is not your turn."})

    def test_not_in_a_game(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.alice.auth_token))
        response = self.client.post(reverse("games:move", args=(0, )))
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.data, {"detail": "Not currently in a game."})


class ForfeitViewTest(APITestCase):

    def setUp(self):
        self.alice = User.objects.create_user("alice", "", "password")
        self.bob = User.objects.create_user("bob", "", "password")

    def test_forfeit(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.alice.auth_token))
        self.client.post(reverse("games:start"))
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.bob.auth_token))
        self.client.post(reverse("games:start"))
        response = self.client.post(reverse("games:forfeit"))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data["winner"], self.alice.pk)

    def test_leave_stalemate(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.alice.auth_token))
        self.client.post(reverse("games:start"))
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.bob.auth_token))
        self.client.post(reverse("games:start"))
        game = Game.current_game(self.alice)
        game.stalemate = True
        game.save()
        response = self.client.post(reverse("games:forfeit"))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data["winner"], None)


    def test_not_in_a_game(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.alice.auth_token))
        response = self.client.get(reverse("games:detail"))
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.data, {"detail": "Not currently in a game."})


class DetailViewTest(APITestCase):

    def setUp(self):
        self.alice = User.objects.create_user("alice", "", "password")

    def test_view_board(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.alice.auth_token))
        self.client.post(reverse("games:start"))
        response = self.client.get(reverse("games:detail"))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data["player1"], self.alice.pk)

    def test_not_in_a_game(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.alice.auth_token))
        response = self.client.get(reverse("games:detail"))
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.data, {"detail": "Not currently in a game."})


class StartViewTest(APITestCase):

    def setUp(self):
        self.alice = User.objects.create_user("alice", "", "password")
        self.bob = User.objects.create_user("bob", "", "password")

    def test_get_a_game(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.alice.auth_token))
        response = self.client.post(reverse("games:start"))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data["player1"], self.alice.pk)

    def test_join_game_second(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.alice.auth_token))
        response = self.client.post(reverse("games:start"))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data["player1"], self.alice.pk)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.bob.auth_token))
        response = self.client.post(reverse("games:start"))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data["player2"], self.bob.pk)
