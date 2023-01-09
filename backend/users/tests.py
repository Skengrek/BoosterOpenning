from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status


class userProfileTestCase(APITestCase):
    profile_list_url = reverse("users-list")

    def setUp(self):
        self.client = APIClient(SERVER_NAME="localhost")

        # create a new user making a post request to djoser endpoint
        self.user = self.client.post(
            "/api/users/", data={"username": "mario", "password": "i-keep-jumping"}
        )
        # obtain a json web token for the newly created user
        response = self.client.post(
            "/auth/jwt/create/",
            data={"username": "mario", "password": "i-keep-jumping"},
        )
        self.token = response.data["access"]
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

    # retrieve a list of all user profiles while the request user is authenticated
    def test_userprofile_list_authenticated(self):
        response = self.client.get(self.profile_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # retrieve a list of all user profiles while the request user is unauthenticated
    def test_userprofile_list_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.profile_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # check to retrieve the profile details of the authenticated user
    def test_userprofile_detail_retrieve(self):
        response = self.client.get(reverse("profile", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
