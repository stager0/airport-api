from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import make_aware
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from airport.models import (
    AirplaneType,
    Airplane,
    Airport,
    Route,
    Crew, Flight
)
from airport.serializers import (
    CrewSerializer,
    AirportSerializer,
    AirplaneSerializer,
    AirplaneTypeSerializer,
    RouteListSerializer,
    FlightListSerializer
)

defaults_flight = {
        "departure_time": make_aware(datetime(2025, 9, 9, 14, 33)),
        "arrival_time": make_aware(datetime(2025, 9, 9, 18, 27)),
        "price_economy": 175,
        "price_business": 280,
        "rows_economy_from": 4,
        "luggage_price_1_kg": 1.99
    }


class BaseCase(TestCase):
    def setUp(self):
        self.airplane_type = AirplaneType.objects.create(name="Passage")
        self.airplane = Airplane.objects.create(name="Boeing", rows=10, letters_in_row="ABCDEFGH", airplane_type=self.airplane_type)
        self.airport = Airport.objects.create(name="International Airport Odessa", closest_big_city="Odessa")
        self.airport1 = Airport.objects.create(name="International Airport Lviv", closest_big_city="Lviv")
        self.route = Route.objects.create(source=self.airport, destination=self.airport1, distance=920)
        self.crew_captain = Crew.objects.create(first_name="Joe" ,last_name="Henrynton", position="CAPTAIN")
        self.crew_first_officer = Crew.objects.create(first_name="Oleg" ,last_name="Berny", position="FIRST_OFFICER")
        self.flight = Flight.objects.create(**defaults_flight, route=self.route, airplane=self.airplane)
        self.flight.crew.set([self.crew_captain, self.crew_first_officer])
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

"""
class AirplaneTypeApiTests(BaseCase):
    def setUp(self):
        super().setUp()
        self.list_url = reverse("airport:airplanetype-list")

    def test_airplane_type_list_status_200_and_contains_value(self):
        response = self.client.get(self.list_url)
        airplane_types = AirplaneType.objects.all()

        serializer = AirplaneTypeSerializer(airplane_types, many=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Passage", 1)
        self.assertEqual(response.data, serializer.data)

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
        airplanes = Airplane.objects.all()

        serializer = AirplaneSerializer(airplanes, many=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Boeing", 1)
        self.assertEqual(response.data, serializer.data)

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

    def test_properties_capacity_and_list_of_seats_and_seats_in_row_count_return_without_mistakes(self):
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
        airports = Airport.objects.all()

        serializer = AirportSerializer(airports, many=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Odessa")
        self.assertEqual(response.data, serializer.data)

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
        routes = Route.objects.all()

        serializer = RouteListSerializer(routes, many=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lviv")
        self.assertEqual(response.data, serializer.data)

    def test_route_str(self):
        self.assertEqual(str(self.route), "Source: International Airport Odessa (Odessa) "
                                          "-> Destination: International Airport Lviv (Lviv)")

    def test_create_route_when_is_staff_false_status_403(self):
        response = self.client.post(self.list_url, {"source": self.airport.id, "destination": self.airport1.id, "distance": 999}, format="json")

        self.assertEqual(response.status_code, 403)

    def test_create_route_when_user_is_staff_status_201(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.super_access_token)
        response = self.client.post(self.list_url, {"source": self.airport.id, "destination": self.airport1.id, "distance": 999}, format="json")

        self.assertEqual(response.status_code, 201)


class CrewApiTests(BaseCase):
    def setUp(self):
        super().setUp()
        self.list_url = reverse("airport:crew-list")

    def test_crew_list_status_200_and_contains_value(self):
        response = self.client.get(self.list_url)
        crews = Crew.objects.all()

        serializer = CrewSerializer(crews, many=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Henrynton")
        self.assertEqual(response.data, serializer.data)

    def test_crew_str(self):
        self.assertEqual(str(self.crew_captain), "Joe Henrynton, Position: Captain")

    def test_crew_property_full_name_and_position(self):
        self.assertEqual(self.crew_captain.full_name_and_position, "Joe Henrynton, Position: Captain")

    def test_create_crew_when_is_staff_false_status_403(self):
        response = self.client.post(self.list_url, {"first_name": "Joe", "last_name": "Joe", "position": "CAPTAIN"}, format="json")

        self.assertEqual(response.status_code, 403)

    def test_create_crew_when_is_staff_true_status_201(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.super_access_token)
        response = self.client.post(self.list_url, {"first_name": "Joe", "last_name": "Joe", "position": "CAPTAIN"}, format="json")

        self.assertEqual(response.status_code, 201)
"""

class FlightApiTests(BaseCase):
    def setUp(self):
        super().setUp()
        self.list_url = reverse("airport:flight-list")

    def test_flight_list_status_200_and_contains_value(self):
        response = self.client.get(self.list_url)
        flights = Flight.objects.all()

        serializer = FlightListSerializer(flights, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "2025-09-09T14:33:00Z")

    def test_flight_str(self):
        self.assertEqual(str(self.flight), "International Airport Odessa -> International Airport Lviv")

    def test_create_flight_when_is_staff_false_status_403(self):
        response = self.client.post(self.list_url, {
            **defaults_flight,
            "airplane": self.airplane.id,
            "route": self.route.id,
            "crew": [self.crew_captain.id, self.crew_first_officer.id]
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_flight_when_is_staff_status_201(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.super_access_token)
        response = self.client.post(self.list_url, {
            **defaults_flight,
            "airplane": self.airplane.id,
            "route": self.route.id,
            "crew": [self.crew_captain.id, self.crew_first_officer.id]
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
