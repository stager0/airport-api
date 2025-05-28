from http.client import responses

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from airport.models import (
    AirplaneType,
    Airplane,
    Airport, Route
)


class BaseCase(TestCase):
    def setUp(self):
        self.airplane_type = AirplaneType.objects.create(name="Passage")
        self.airplane = Airplane.objects.create(name="Boeing", rows=10, letters_in_row="ABCDEFGH", airplane_type=self.airplane_type)
        self.airport = Airport.objects.create(name="International Airport Odessa", closest_big_city="Odessa")
        self.airport1 = Airport.objects.create(name="International Airport Lviv", closest_big_city="Lviv")
        self.route = Route.objects.create(source=self.airport, destination=self.airport1, distance=920)
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

    def test_airplane_type_list_status_200_and_contains_value(self):
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

    def test_airplane_list_status_200_and_contains_value(self):
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

    def test_create_when_user_is_staff_status_201(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.super_access_token)
        response = self.client.post(self.list_url, {
            "name": "test1",
            "rows": 21,
            "letters_in_row": "ABCD",
            "airplane_type": self.airplane_type.id
        }, format="json")

        self.assertEqual(response.status_code, 201)

    def test_airplane_str(self):
        self.assertEqual(str(self.airplane), "Boeing, rows: 10, letters in row: ABCDEFGH")

    def test_properties_capacity_list_of_seats_seats_in_row_count_return_without_mistakes(self):
        airplane = self.airplane

        self.assertEqual(airplane.capacity, 80)
        self.assertEqual(airplane.list_of_seats, ["A", "B", "C", "D", "E", "F", "G", "H"])
        self.assertEqual(airplane.seats_in_row_count, 8)


class AirportApiTests(BaseCase):
    def setUp(self):
        super().setUp()
        self.list_url = reverse("airport:airport-list")

    def test_airport_list_status_200_and_contains_value(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Odessa")

    def test_airport_str(self):
        self.assertEqual(str(self.airport), "International Airport Odessa, city: (Odessa)")

    def test_create_without_is_staff_status_403(self):
        response = self.client.post(self.list_url, {"name": "Krymea International Airport", "closest_big_city": "Krymea"})

        self.assertEqual(response.status_code, 403)

    def test_airport_create_when_user_is_staff_status_201(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.super_access_token)
        response = self.client.post(self.list_url, {"name": "Krymea International Airport", "closest_big_city": "Krymea"}, format="json")

        self.assertEqual(response.status_code, 201)


class RouteApiTest(BaseCase):
    def setUp(self):
        super().setUp()
        self.list_url = reverse("airport:route-list")

    def test_route_list_status_200_and_contains_value(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lviv")

    def test_route_str(self):
        self.assertEqual(str(self.route), "Source: International Airport Odessa (Odessa) "
                                          "-> Destination: International Airport Lviv (Lviv)")

    def test_create_route_when_is_staff_false_status_403(self):
        response = self.client.post(self.list_url, {"source": self.airport, "destination": self.airport1, "distance": 999})

        self.assertEqual(response.status_code, 403)