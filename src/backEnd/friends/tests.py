"""
All test cases for accounts section of app.
"""

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from friends.models import Follower
from accounts.serializers import UserSerializer


class IndexViewTests(APITestCase):

    def setUp(self):
        self.alice = User.objects.create_user("alice", "", "password")
        self.bob = User.objects.create_user("bob", "", "password")
        self.casey = User.objects.create_user("casey", "", "password")

    def test_no_friends(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.alice.auth_token))
        response = self.client.get(reverse("friends:index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_one_friend(self):
        Follower.objects.create(follower=self.alice, followed=self.bob)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.alice.auth_token))
        response = self.client.get(reverse("friends:index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [UserSerializer(self.bob).data])

    def test_multiple_friends(self):
        Follower.objects.create(follower=self.alice, followed=self.bob)
        Follower.objects.create(follower=self.alice, followed=self.casey)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.alice.auth_token))
        response = self.client.get(reverse("friends:index"))
        self.assertEqual(response.status_code, 200)
        bob_data = UserSerializer(self.bob).data
        casey_data = UserSerializer(self.casey).data
        self.assertItemsEqual(response.data, [bob_data, casey_data])


class AddViewTests(APITestCase):

    def setUp(self):
        self.alice = User.objects.create_user("alice", "", "password")
        self.bob = User.objects.create_user("bob", "", "password")
        self.casey = User.objects.create_user("casey", "", "password")

    def test_add_friend(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.alice.auth_token))
        response = self.client.post(reverse("friends:add"), {"id": self.bob.pk})
        assert Follower.objects.get(follower=self.alice, followed=self.bob)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [UserSerializer(self.bob).data])

    def test_add_duplicate_friend(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.alice.auth_token))
        response_1 = self.client.post(reverse("friends:add"), {"id": self.bob.pk})
        assert Follower.objects.get(follower=self.alice, followed=self.bob)
        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(response_1.data, [UserSerializer(self.bob).data])
        response_2 = self.client.post(reverse("friends:add"), {"id": self.bob.pk})
        self.assertEqual(response_2.status_code, 200)
        self.assertEqual(Follower.objects.filter(follower=self.alice).count(), 1)

    def test_add_self(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.alice.auth_token))
        response = self.client.post(reverse("friends:add"), {"id": self.alice.pk})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"detail": "Cannot add self."})
        self.assertEqual(Follower.objects.filter(follower=self.alice).count(), 0)

    def test_no_id(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.alice.auth_token))
        response = self.client.post(reverse("friends:add"), {})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"detail": "Must provide id."})
        self.assertEqual(Follower.objects.filter(follower=self.alice).count(), 0)

    def test_id_out_of_range(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.alice.auth_token))
        response = self.client.post(reverse("friends:add"), {"id": 4})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"detail": "Invalid user id."})
        self.assertEqual(Follower.objects.filter(follower=self.alice).count(), 0)
