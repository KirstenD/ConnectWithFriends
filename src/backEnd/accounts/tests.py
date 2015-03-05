"""
All test cases for accounts section of app.
"""

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from accounts.serializers import UserSerializer


def create_user(username, password):
    """ Create a user with just a username and password.
    """
    return User.objects.create_user(username, '', password)


class LoginViewTests(APITestCase):

    def test_get_token_for_existing_user(self):
        username = "Jane Doe"
        password = "password"
        create_user(username, password)
        response = self.client.post(reverse("accounts:login"),
                {'username': username, "password": password})
        self.assertEqual(response.status_code, 200)
        assert "token" in response.data

    def test_get_token_for_nonexisting_user(self):
        username = "Jane Doe"
        password = "password"
        response = self.client.post(reverse("accounts:login"),
                {'username': username, "password": password})
        self.assertEqual(response.status_code, 400)
        assert "Unable to log in with provided credentials." in response.content

    def test_loggin_with_wrong_password(self):
        username = "Jane Doe"
        password = "password"
        wrong_password = "passw0rd"
        create_user(username, password)
        response = self.client.post(reverse("accounts:login"),
                {'username': username, "password": wrong_password})
        self.assertEqual(response.status_code, 400)
        self.assertContains(
            response,
            "Unable to log in with provided credentials.",
            status_code=400)


class CreateViewTests(APITestCase):
    
    def test_create_user(self):
        username = "Jane Doe"
        password = "password"
        response = self.client.post(reverse("accounts:create"),
                {'username': username, "password": password})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "token")

    def test_create_user_no_username(self):
        password = "password"
        response = self.client.post(reverse("accounts:create"),
                {"password": password})
        self.assertEqual(response.status_code, 400)
        self.assertContains(
            response,
            "Username or password not specified",
            status_code=status.HTTP_400_BAD_REQUEST)

    def test_create_user_no_password(self):
        username = "Jane Doe"
        response = self.client.post(reverse("accounts:create"),
                {'username': username})
        self.assertEqual(response.status_code, 400)
        self.assertContains(
            response,
            "Username or password not specified",
            status_code=status.HTTP_400_BAD_REQUEST)

    def test_create_user_already_exists(self):
        username = "Jane Doe"
        password = "password"
        create_user(username, password)
        new_password = "someotherpassword"
        response = self.client.post(reverse("accounts:create"),
                {'username': username, "password": new_password})
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertContains(
            response,
            "Username already taken.",
            status_code=status.HTTP_409_CONFLICT)


class WhoamiViewTests(APITestCase):

    def test_valid_token(self):
        username = "Jane Doe"
        password = "password"
        user = create_user(username, password)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(user.auth_token))
        response = self.client.get(reverse("accounts:whoami"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], username)

    def test_no_token(self):
        response = self.client.get(reverse("accounts:whoami"))
        self.assertEqual(response.status_code, 401)
        self.assertContains(
            response,
            "Authentication credentials were not provided",
            status_code=401)

    def test_invalid_token(self):
        username = "Jane Doe"
        password = "password"
        create_user(username, password)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + "notatoken")
        response = self.client.get(reverse("accounts:whoami"))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["detail"], "Invalid token")


class DetailViewTests(APITestCase):

    def setUp(self):
        self.user = create_user("Jane Doe", "password")

    def test_get_user(self):
        response = self.client.get(reverse("accounts:detail",
                                           kwargs={"user_id": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, UserSerializer(self.user).data)

    def test_invalid_id(self):
        response = self.client.get(reverse("accounts:detail",
                                           kwargs={"user_id": 2}))
        self.assertEqual(response.status_code, 404)
