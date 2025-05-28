from http.client import responses

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from airport.models import AirplaneType, Airplane


class BaseCase(TestCase):
    def setUp(self):
        self.airplane_type = AirplaneType.objects.create(name="Passage")
        self.airplane = Airplane.objects.create(name="Boeing", rows=199, letters_in_row="ABCDEFGH", airplane_type=self.airplane_type)
        self.user = get_user_model().objects.create_user(
            email="test_email@test.com",
            first_name="Vasyl",
            last_name="Muller",
            password="1qazcde3"
        )
        self.superuser = get_user_model().objects.create_superuser(
            email="test_email1@test.com",
            first_name="Oleg",
            last_name="Grynko",
            password="1qazcde3"
        )
        refresh = RefreshToken.for_user(self.user)
        refresh_super = RefreshToken.for_user(self.superuser)
        self.access_token = str(refresh.access_token)
        self.super_access_token = str(refresh_super.access_token)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)


class AirplaneTypeApiTests(BaseCase):
    def setUp(self):
        super().setUp()
        self.list_url = reverse("airport:airplanetype-list")

    def test_airplane_type_list(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Passage", 1)

    def test_airplane_type_create_200(self):
        response = self.client.post(self.list_url, {"name": "TEST"}, format="json")

        self.assertEqual(response.status_code, 403)

    def test_airplane_type_create_403(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.super_access_token)
        response = self.client.post(self.list_url, {"name": "TEST"}, format="json")

        self.assertEqual(response.status_code, 201)

class AirplaneApiTests(BaseCase):
    def setUp(self):
        super().setUp()
        self.list_url = reverse("airport:airplane-list")

    def test_airplane_list_200(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Boeing", 1)

    def test_create_airplane_without_is_staff_status_403(self):
        response =self.client.post(self.list_url, {
            "name": "test",
            "rows": 22,
            "letters_in_row": "ABC",
            "airplane_type": self.airplane_type
        })
        self.assertEqual(response.status_code, 403)
