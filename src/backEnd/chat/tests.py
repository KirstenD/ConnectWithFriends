"""
All test cases for chat app.
"""
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APITestCase

from chat.models import GlobalMessage, GameMessage


class SendGlobalMessageViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user("Jane Doe", "", "password")

    def test_send_message(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.user.auth_token))
        response = self.client.post(reverse("chat:send"), 
                {"text": "test message"}, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["sender"], 1)
        self.assertEqual(response.data["text"], "test message")

    def test_no_auth_token(self):
        response = self.client.post(
            reverse("chat:send"),
            {"text": "test message"})
        self.assertEqual(response.status_code, 401)
        self.assertContains(response,
            "Authentication credentials were not provided",
            status_code=401)

    def test_no_message_text(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.user.auth_token))
        response = self.client.post(reverse("chat:send"), {}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["text"], ["This field is required."])


class GlobalMessageListViewTests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user("Jane Doe", "", "password")
        self.user2 = User.objects.create_user("John Doe", "", "password")

    def test_no_messages(self):
        response = self.client.get(reverse("chat:index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_many_messages(self):
        GlobalMessage.objects.create(
            sender=self.user1,
            text="This is a test message",
            pub_date=timezone.now())
        GlobalMessage.objects.create(
            sender=self.user2,
            text="This is another test message",
            pub_date=timezone.now())
        response = self.client.get(reverse("chat:index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["sender"], 1)
        self.assertEqual(response.data[0]["text"], "This is a test message")
        self.assertEqual(response.data[1]["sender"], 2)


class SendGameMessageViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user("Jane Doe", "", "password")

    def test_send_message(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.user.auth_token))
        self.client.post(reverse("games:start"))
        response = self.client.post(reverse("chat:game_send"), {"text": "test message"}, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["sender"], 1)
        self.assertEqual(response.data["text"], "test message")
        self.assertEqual(GameMessage.objects.all().count(), 1)

    def test_not_in_game(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.user.auth_token))
        response = self.client.post(reverse("chat:game_send"), {"text": "test message"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["detail"], "You are not in a game.")

    def test_no_message_text(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.user.auth_token))
        self.client.post(reverse("games:start"))
        response = self.client.post(reverse("chat:game_send"), {}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["text"], ["This field is required."])


class GameMessageListViewTests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user("Jane Doe", "", "password")
        self.user2 = User.objects.create_user("John Doe", "", "password")

    def test_not_in_game(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.user1.auth_token))
        response = self.client.get(reverse("chat:game_index"))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["detail"], "You are not in a game.")

    def test_no_messages(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.user1.auth_token))
        self.client.post(reverse("games:start"))
        response = self.client.get(reverse("chat:game_index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_many_messages(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.user1.auth_token))
        self.client.post(reverse("games:start"))
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.user2.auth_token))
        self.client.post(reverse("games:start"))
        self.client.post(reverse("chat:game_send"), {"text": "player2 message"}, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.user1.auth_token))
        self.client.post(reverse("chat:game_send"), {"text": "player1 message"}, format="json")
        response = self.client.get(reverse("chat:game_index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["sender"], self.user2.pk)
        self.assertEqual(response.data[0]["text"], "player2 message")
        self.assertEqual(response.data[1]["sender"], self.user1.pk)
        self.assertEqual(response.data[1]["text"], "player1 message")
