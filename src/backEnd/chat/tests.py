"""
All test cases for chat app.
"""
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status

from chat.models import GlobalMessage


class SendGlobalMessageViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user("Jane Doe", "", "password")

    def test_send_message(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.user.auth_token))
        response = self.client.post(reverse("chat:detail"), 
                {"text": "test message"}, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["sender"], 1)
        self.assertEqual(response.data["text"], "test message")

    def test_no_auth_token(self):
        response = self.client.post(
            reverse("chat:detail"),
            {"text": "test message"})
        self.assertEqual(response.status_code, 401)
        self.assertContains(response,
            "Authentication credentials were not provided",
            status_code=401)

    def test_no_message_text(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.user.auth_token))
        response = self.client.post(reverse("chat:detail"), {}, format="json")
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
