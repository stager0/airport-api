import copy
import tempfile
from datetime import datetime
from decimal import Decimal
from http.client import responses

from PIL import Image
from django.contrib.auth import get_user_model
from django.db.models import Count, F
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import make_aware
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from airport.models import (
    AirplaneType,
    Airplane,
    Airport,
    Route,
    Crew, Flight, SnacksAndDrinks, MealOption, ExtraEntertainmentAndComfort, DiscountCoupon, Ticket, Order
)
from airport.serializers import (
    CrewSerializer,
    AirportSerializer,
    AirplaneSerializer,
    AirplaneTypeSerializer,
    RouteListSerializer,
    FlightListSerializer,
    OrderListSerializer,
    SnacksAndDrinksSerializer,
    MealOptionSerializer,
    ExtraEntertainmentAndComfortSerializer,
    DiscountCouponSerializer, DISCOUNT_FOR_CHILDREN, OrderSerializer, OrderRetrieveSerializer
)

defaults_flight = {
    "departure_time": make_aware(datetime(2025, 9, 9, 14, 33)),
    "arrival_time": make_aware(datetime(2025, 9, 9, 18, 27)),
    "price_economy": 175,
    "price_business": 280,
    "rows_economy_from": 4,
    "luggage_price_1_kg": 1.99
}


def sample_ticket(**params):
    defaults = {
        "row": 9,
        "letter": "A",
        "has_luggage": True,
        "luggage_weight": 10,
        "flight": Flight.objects.first(),
        "order": Order.objects.create(user=get_user_model().objects.first()),
        "meal_option": MealOption.objects.first(),
        "discount_coupon": DiscountCoupon.objects.first()
    }
    defaults.update(**params)
    ticket = Ticket.objects.create(**defaults)
    ticket.extra_entertainment_and_comfort.set([ExtraEntertainmentAndComfort.objects.first().id])
    ticket.snacks_and_drinks.set([SnacksAndDrinks.objects.first().id])
    return ticket


def generate_image_for_tests():
    image_to_upload = Image.new("RGB", (150, 150), color="green")
    temporary_file = tempfile.TemporaryFile(suffix=".jpg")
    image_to_upload.save(temporary_file, format="JPEG")
    temporary_file.seek(0)
    return temporary_file


class BaseCase(TestCase):
    def setUp(self):
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
        self.airplane_type = AirplaneType.objects.create(name="Passage")
        self.airplane = Airplane.objects.create(name="Boeing", rows=10, letters_in_row="ABCDEFGH",
                                                airplane_type=self.airplane_type)
        self.airport = Airport.objects.create(name="International Airport Odessa", closest_big_city="Odessa")
        self.airport1 = Airport.objects.create(name="International Airport Lviv", closest_big_city="Lviv")
        self.airport2 = Airport.objects.create(name="International Airport Paris", closest_big_city="Paris")
        self.route = Route.objects.create(source=self.airport, destination=self.airport1, distance=920)
        self.route1 = Route.objects.create(source=self.airport2, destination=self.airport, distance=1900)
        self.crew_captain = Crew.objects.create(first_name="Joe", last_name="Henrynton", position="CAPTAIN")
        self.crew_first_officer = Crew.objects.create(first_name="Oleg", last_name="Berny", position="FIRST_OFFICER")
        self.flight = Flight.objects.create(**defaults_flight, route=self.route, airplane=self.airplane)
        self.flight.crew.set([self.crew_captain, self.crew_first_officer])
        self.snacks_and_drinks = SnacksAndDrinks.objects.create(name="Chips", price=2.99)
        self.meal_option = MealOption.objects.create(name="Borsch", meal_type=1, weight=300, price=8.99)
        self.meal_option1 = MealOption.objects.create(name="Pasta", meal_type=3, weight=440, price=10.99)
        self.extra = ExtraEntertainmentAndComfort.objects.create(name="Tablet Ipad (45 games)", price=4.99)
        self.extra1 = ExtraEntertainmentAndComfort.objects.create(name="Pillow", price=1.99)
        self.discount_coupon = DiscountCoupon.objects.create(
            name="Summer Action",
            valid_until=make_aware(datetime(2025, 9, 9, 15)),
            code="SUMMER9999",
            discount=30,
        )
        self.ticket_economy = sample_ticket()
        self.ticket_business = sample_ticket(**{"row": 1, "order": Order.objects.create(user=self.superuser)})

        refresh = RefreshToken.for_user(self.user)
        refresh_super = RefreshToken.for_user(self.superuser)
        self.access_token = str(refresh.access_token)
        self.super_access_token = str(refresh_super.access_token)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)



class OrderApiTests(BaseCase):
    def setUp(self):
        super().setUp()
        self.list_url = reverse("airport:order-list")
        self.defaults_ticket_json = {
            "user": self.user.id,
            "tickets": [
                {
                "row": 9,
                "letter": "B",
                "has_luggage": True,
                "luggage_weight": 10,
                "flight": self.flight.id,
                "meal_option": self.meal_option.id,
                "discount_coupon": self.discount_coupon.code,
                "extra_entertainment_and_comfort": [self.extra.id],
                "snacks_and_drinks": [self.snacks_and_drinks.id]
                }
            ]
        }

    def test_order_list_status_200_and_contains_value(self):
        response = self.client.get(self.list_url)
        orders = Order.objects.filter(user=self.user).annotate(
            count_of_tickets=Count(
                "tickets"
            ), source=F(
                "tickets__flight__route__source__closest_big_city"
            ), destination=F(
                "tickets__flight__route__destination__closest_big_city"
            )).order_by("id")
        serializer = OrderListSerializer(orders, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_order_str(self):
        order = Order.objects.first()
        self.assertEqual(str(order), timezone.now().strftime("%Y-%m-%d %H:%M"))

    def test_create_order_when_is_staff_false_status_201(self):
        response = self.client.post(self.list_url, self.defaults_ticket_json, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_order_without_user_status_400(self):
        default_ticket_json_without_user = self.defaults_ticket_json.update(**{"user": None})
        response = self.client.post(self.list_url, default_ticket_json_without_user, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_without_extra_entertainment_and_snacks_status_201(self):
        tickets_without_extra_and_snacks = copy.deepcopy(self.defaults_ticket_json)
        tickets_without_extra_and_snacks["tickets"][0]["extra_entertainment_and_comfort"] = []
        tickets_without_extra_and_snacks["tickets"][0]["snacks_and_drinks"] = []

        response = self.client.post(self.list_url, tickets_without_extra_and_snacks, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_order_ticket_without_meal_option_status_400(self):
        ticket_dict_without_meal_option = copy.deepcopy(self.defaults_ticket_json)
        ticket_dict_without_meal_option["tickets"][0]["meal_option"] = None

        response = self.client.post(self.list_url, ticket_dict_without_meal_option, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_with_not_available_place_status_400(self):
        ticket_with_place_out_range = copy.deepcopy(self.defaults_ticket_json)
        # letters are ABCDEFGH
        ticket_with_place_out_range["tickets"][0]["letter"] = "Q" # ----> wrong letter

        response = self.client.post(self.list_url, ticket_with_place_out_range, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_with_wrong_validate_coupon_status_400(self):
        ticket_with_wrong_coupon = copy.deepcopy(self.defaults_ticket_json)
        ticket_with_wrong_coupon["tickets"][0]["discount_coupon"] = "WRONG COUPON"

        response = self.client.post(self.list_url, ticket_with_wrong_coupon, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_without_discount_coupon_status_201(self):
        ticket_without_coupon = copy.deepcopy(self.defaults_ticket_json)
        ticket_without_coupon["tickets"][0]["discount_coupon"] = None

        response = self.client.post(self.list_url, ticket_without_coupon, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_order_with_discount_coupon_status_201_and_ticket_has_discount(self):
        ticket_with_active_coupon = copy.deepcopy(self.defaults_ticket_json)
        code = "SUMMER9999"
        ticket_with_active_coupon["tickets"][0]["discount_coupon"] = code

        response = self.client.post(self.list_url, ticket_with_active_coupon, format="json")

        expected_discount = Decimal(DiscountCoupon.objects.get(code=code).discount)
        actual_discount = Decimal(response.data["tickets"][0]["discount"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(actual_discount, expected_discount)

    def test_create_ticket_with_occupied_place_status_400(self):
        ticket_with_occupied_place = copy.deepcopy(self.defaults_ticket_json)
        ticket_with_occupied_place["tickets"][0]["row"] = 9
        ticket_with_occupied_place["tickets"][0]["letter"] = "A"

        response = self.client.post(self.list_url, ticket_with_occupied_place, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_ticket_if_row_is_out_range_status_400(self):
        ticket_with_row_out_range = copy.deepcopy(self.defaults_ticket_json)
        ticket_with_row_out_range["tickets"][0]["row"] = 99999 # ------> wrong row, its more than there is

        response = self.client.post(self.list_url, ticket_with_row_out_range, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_if_has_luggage_is_false_but_luggage_weight_more_than_0_status_201(self):
        # logic must by itself change has_luggage to True in this situation
        ticket_has_luggage_is_false_but_has_luggage_weight = copy.deepcopy(self.defaults_ticket_json)
        ticket_has_luggage_is_false_but_has_luggage_weight["tickets"][0]["has_luggage"] = False
        ticket_has_luggage_is_false_but_has_luggage_weight["tickets"][0]["luggage_weight"] = 50

        response = self.client.post(
            self.list_url,
            ticket_has_luggage_is_false_but_has_luggage_weight,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["tickets"][0]["has_luggage"], True)
        self.assertEqual(float(response.data["tickets"][0]["luggage_weight"]), float(50))

    def test_create_empty_order_status_400(self):
        no_tickets = {
            "tickets": []
        }
        response = self.client.post(self.list_url, no_tickets, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_ticket_for_child_discount_50_status_201(self):
        ticket_child = copy.deepcopy(self.defaults_ticket_json)
        ticket_child["tickets"][0]["is_child"] = True
        ticket_child["tickets"][0]["discount_coupon"] = None
        response = self.client.post(self.list_url, ticket_child, format="json")

        self.assertEqual(response.data["tickets"][0]["discount"], DISCOUNT_FOR_CHILDREN)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_order_not_admin_status_200(self):
        order = Order.objects.first()
        url = reverse("airport:order-detail", args=[order.id])
        response = self.client.get(url)
        serializer = OrderRetrieveSerializer(order)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


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
        self.upload_url = reverse("airport:airplane-upload-image", args=[self.airplane.id])

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

    def test_upload_image_to_airplane_when_user_is_staff_status_200(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.super_access_token)
        image = generate_image_for_tests()

        response = self.client.post(self.upload_url, {
            "image": image
        }, format="multipart")

        self.assertEqual(response.status_code, 200)
        self.assertIn("image", response.data)
        self.assertTrue(response.data["image"].endswith(".jpg"))

    def test_upload_image_when_user_is_not_staff_status_403(self):
        image = generate_image_for_tests()

        response = self.client.post(self.upload_url, {"image": image}, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


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

    def test_airport_filter_by_closest_big_city(self):
        response = self.client.get(self.list_url, {"closest_big_city": f"{self.airport.closest_big_city}"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["closest_big_city"], self.airport.closest_big_city)
        self.assertNotEqual(response.data[0]["closest_big_city"], self.airport1.closest_big_city)

    def test_airport_filter_by_airport_name(self):
        response = self.client.get(self.list_url, {"name": f"{self.airport.name}"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], str(self.airport.name))
        self.assertNotEqual(response.data[0]["name"], self.airport1.name)

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

    def test_route_filter_by_source(self):
        response = self.client.get(self.list_url, {"source": f"{self.route.source.closest_big_city}"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["source"]["closest_big_city"], self.route.source.closest_big_city)
        self.assertNotEqual(response.data[0]["source"]["closest_big_city"], self.route1.source.closest_big_city)

    def test_route_filter_by_destination(self):
        response = self.client.get(self.list_url, {"destination": f"{self.route.destination.closest_big_city}"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["destination"]["closest_big_city"], self.route.destination.closest_big_city)
        self.assertNotEqual(response.data[0]["destination"]["closest_big_city"], self.route1.destination.closest_big_city)

    def test_route_filter_by_source_airport(self):
        response = self.client.get(self.list_url, {"source_airport": f"{self.route.source.name}"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["source"]["name"], self.route.source.name)
        self.assertNotEqual(response.data[0]["source"]["name"], self.route1.source.name)

    def test_route_filter_by_destination_airport(self):
        response = self.client.get(self.list_url, {"destination_airport": f"{self.route.destination.name}"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["destination"]["name"], self.route.destination.name)
        self.assertNotEqual(response.data[0]["destination"]["name"], self.route1.destination.name)

    def test_create_route_when_is_staff_false_status_403(self):
        response = self.client.post(self.list_url,
                                    {"source": self.airport.id, "destination": self.airport1.id, "distance": 999},
                                    format="json")

        self.assertEqual(response.status_code, 403)

    def test_create_route_when_user_is_staff_status_201(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.super_access_token)
        response = self.client.post(self.list_url,
                                    {"source": self.airport.id, "destination": self.airport1.id, "distance": 999},
                                    format="json")

        self.assertEqual(response.status_code, 201)



class CrewApiTests(BaseCase):
    def setUp(self):
        super().setUp()
        self.list_url = reverse("airport:crew-list")
        self.upload_url = reverse("airport:crew-upload-image", args=[self.crew_captain.id])

    def test_crew_list_status_200_and_contains_value(self):
        response = self.client.get(self.list_url)
        crews = Crew.objects.all()

        serializer = CrewSerializer(crews, many=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Henrynton")
        self.assertEqual(response.data, serializer.data)

    def test_crew_str(self):
        self.assertEqual(str(self.crew_captain), "Joe Henrynton, Position: Captain")

    def test_airport_filter_by_first_name(self):
        response = self.client.get(self.list_url, {"first_name": f"{self.crew_captain.first_name}"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["first_name"], self.crew_captain.first_name)
        self.assertNotEqual(response.data[0]["first_name"], self.crew_first_officer.first_name)

    def test_airport_filter_by_last_name(self):
        response = self.client.get(self.list_url, {"last_name": f"{self.crew_captain.last_name}"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["last_name"], str(self.crew_captain.last_name))
        self.assertNotEqual(response.data[0]["last_name"], self.crew_first_officer.last_name)

    def test_airport_filter_by_position(self):
        response = self.client.get(self.list_url, {"position": f"{self.crew_captain.position}"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["position"], str(self.crew_captain.position))
        self.assertNotEqual(response.data[0]["position"], self.crew_first_officer.position)

    def test_crew_property_full_name_and_position(self):
        self.assertEqual(self.crew_captain.full_name_and_position, "Joe Henrynton, Position: Captain")

    def test_create_crew_when_is_staff_false_status_403(self):
        response = self.client.post(self.list_url, {"first_name": "Joe", "last_name": "Joe", "position": "CAPTAIN"}, format="json")

        self.assertEqual(response.status_code, 403)

    def test_create_crew_when_is_staff_true_status_201(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.super_access_token)
        response = self.client.post(self.list_url, {"first_name": "Joe", "last_name": "Joe", "position": "CAPTAIN"}, format="json")

        self.assertEqual(response.status_code, 201)

    def test_upload_image_to_crew_when_user_is_staff_status_200(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.super_access_token)
        image = generate_image_for_tests()

        response = self.client.post(self.upload_url, {"image": image}, format="multipart")

        self.assertEqual(response.status_code, 200)
        self.assertIn("image", response.data)
        self.assertTrue(response.data["image"].endswith(".jpg"))

    def test_upload_image_to_crew_when_user_is_not_staff_status_403(self):
        image = generate_image_for_tests()

        response = self.client.post(self.upload_url, {"image": image}, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


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


class SnacksAndDrinksApiTests(BaseCase):
    def setUp(self):
        super().setUp()
        self.list_url = reverse("airport:snacksanddrinks-list")
        self.upload_url = reverse("airport:snacksanddrinks-upload-image", args=[self.snacks_and_drinks.id])

    def test_snacks_list_status_200_and_contains_value(self):
        response = self.client.get(self.list_url)
        snacks = SnacksAndDrinks.objects.all()

        serializer = SnacksAndDrinksSerializer(snacks, many=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Chips")
        self.assertEqual(response.data, serializer.data)

    def test_snacks_str(self):
        self.assertEqual(str(self.snacks_and_drinks), f"{self.snacks_and_drinks.name}, PRICE={self.snacks_and_drinks.price}$")

    def test_create_snacks_when_is_staff_false_status_403(self):
        response = self.client.post(self.list_url, {"name": "Tuc", "price": 3.99}, format="json")

        self.assertEqual(response.status_code, 403)

    def test_create_snacks_when_is_staff_true_status_201(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.super_access_token)
        response = self.client.post(self.list_url, {"name": "Tuc", "price": 3.99}, format="json")

        self.assertEqual(response.status_code, 201)

    def test_upload_image_to_snacks_when_user_is_staff_status_200(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.super_access_token)
        image = generate_image_for_tests()

        response = self.client.post(self.upload_url, {
            "image": image
        }, format="multipart")

        self.assertEqual(response.status_code, 200)
        self.assertIn("image", response.data)
        self.assertTrue(response.data["image"].endswith(".jpg"))

    def test_upload_image_to_snacks_when_user_is_not_staff_status_403(self):
        image = generate_image_for_tests()

        response = self.client.post(self.upload_url, {"image": image}, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class MealOptionApiTests(BaseCase):
    def setUp(self):
        super().setUp()
        self.list_url = reverse("airport:mealoption-list")
        self.upload_url = reverse("airport:mealoption-upload-image", args=[self.meal_option.id])

    def test_meal_option_list_status_200_and_contains_value(self):
        response = self.client.get(self.list_url)
        meal_options = MealOption.objects.all()

        serializer = MealOptionSerializer(meal_options, many=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Borsch")
        self.assertEqual(response.data, serializer.data)

    def test_meal_option_str(self):
        self.assertEqual(str(self.meal_option),
            f"Name: {self.meal_option.name},"
            f" type: {self.meal_option.get_meal_type_display()},"
            f" weight: {self.meal_option.weight}, "
            f"PRICE={self.meal_option.price}$"
        )

    def test_create_meal_option_when_is_staff_false_status_403(self):
        response = self.client.post(self.list_url, {
            "name": "Pasta",
            "meal_type": 1,
            "price": 19.99,
            "weight": 300
        }, format="json")

        self.assertEqual(response.status_code, 403)

    def test_meal_option_filter_by_price(self):
        response = self.client.get(self.list_url, {"price": f"{self.meal_option.price}"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(float(response.data[0]["price"]), float(self.meal_option.price))
        self.assertNotEqual(float(response.data[0]["price"]), float(self.meal_option1.price))

    def test_meal_option_filter_by_name(self):
        response = self.client.get(self.list_url, {"name": f"{self.meal_option.name}"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], self.meal_option.name)
        self.assertNotEqual(response.data[0]["name"], self.meal_option1.name)

    def test_meal_option_filter_by_meal_type(self):
        response = self.client.get(self.list_url, {"meal_type": 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["meal_type"], str(self.meal_option.meal_type))
        self.assertNotEqual(response.data[0]["meal_type"], self.meal_option1.meal_type)

    def test_create_meal_option_when_is_staff_true_status_201(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.super_access_token)
        response = self.client.post(self.list_url, {
            "name": "Pasta Carbonara",
            "meal_type": 1,
            "price": 19.99,
            "weight": 300
        }, format="json")

        self.assertEqual(response.status_code, 201)

    def test_upload_image_to_meal_option_when_user_is_staff_status_200(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.super_access_token)
        image = generate_image_for_tests()

        response = self.client.post(self.upload_url, {
            "image": image
        }, format="multipart")

        self.assertEqual(response.status_code, 200)
        self.assertIn("image", response.data)
        self.assertTrue(response.data["image"].endswith(".jpg"))

    def test_upload_image_to_meal_option_when_user_is_not_staff_status_403(self):
        image = generate_image_for_tests()

        response = self.client.post(self.upload_url, {"image": image}, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ExtraEntertainmentAndComfortApiTests(BaseCase):
    def setUp(self):
        super().setUp()
        self.list_url = reverse("airport:extraentertainmentandcomfort-list")
        self.upload_url = reverse("airport:extraentertainmentandcomfort-upload-image", args=[self.extra.id])

    def test_extra_list_status_200_and_contains_value(self):
        response = self.client.get(self.list_url)
        extra = ExtraEntertainmentAndComfort.objects.all()

        serializer = ExtraEntertainmentAndComfortSerializer(extra, many=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tablet Ipad (45 games)")
        self.assertEqual(response.data, serializer.data)

    def test_extra_str(self):
        self.assertEqual(str(self.extra), f"{self.extra.name} -> {self.extra.price}$")

    def test_extra_filter_by_name(self):
        response = self.client.get(self.list_url, {"name": {self.extra.name}})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], self.extra.name)
        self.assertNotEqual(response.data[0]["name"], self.extra1.name)

    def test_create_extra_when_is_staff_false_status_403(self):
        response = self.client.post(self.list_url, {"name": "Pillow", "price": 2.99}, format="json")

        self.assertEqual(response.status_code, 403)

    def test_create_extra_when_is_staff_true_status_201(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.super_access_token)
        response = self.client.post(self.list_url, {"name": "Pillow", "price": 2.99}, format="json")

        self.assertEqual(response.status_code, 201)

    def test_upload_image_to_extra_entertainment_when_user_is_staff_status_200(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.super_access_token)
        image = generate_image_for_tests()

        response = self.client.post(self.upload_url, {
            "image": image
        }, format="multipart")

        self.assertEqual(response.status_code, 200)
        self.assertIn("image", response.data)
        self.assertTrue(response.data["image"].endswith(".jpg"))

    def test_upload_image_to_extra_entertainment_when_user_is_not_staff_status_403(self):
        image = generate_image_for_tests()

        response = self.client.post(self.upload_url, {"image": image}, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DiscountCouponApiTests(BaseCase):
    def setUp(self):
        super().setUp()
        self.list_url = reverse("airport:discountcoupon-list")

    def test_discount_coupon_list_status_200_and_contains_value(self):
        response = self.client.get(self.list_url)
        discount_coupons = DiscountCoupon.objects.all()

        serializer = DiscountCouponSerializer(discount_coupons, many=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Summer Action")
        self.assertEqual(response.data, serializer.data)

    def test_discount_coupon_str(self):
        self.assertEqual(str(self.discount_coupon), f"Coupon Name: {self.discount_coupon.name}, Code: {self.discount_coupon.code}")

    def test_create_discount_coupon_with_invalid_code(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.super_access_token)
        response = self.client.post(self.list_url, {
            "name": "INVALID",
            "valid_until": make_aware(datetime(2099, 1, 1, 0, 1)),
            "code": "invalid",
            "discount": 25
        },
        format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_discount_coupon_when_is_staff_false_status_403(self):
        response = self.client.post(self.list_url, {
            "name": "New Year 2025",
            "valid_until": make_aware(datetime(2026, 1, 1, 0, 1)),
            "code": "NEWYEAR777",
            "discount": 25
        },
        format="json")

        self.assertEqual(response.status_code, 403)

    def test_create_discount_coupon_when_is_staff_true_status_201(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.super_access_token)
        response = self.client.post(self.list_url, {
            "name": "Christmas 2025",
            "valid_until": make_aware(datetime(2025, 12, 30)),
            "code": "NEWYEAR777",
            "discount": 35
        },
        format="json")

        self.assertEqual(response.status_code, 201)

    def test_create_discount_code_if_valid_until_earlier_than_now(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.super_access_token)
        response = self.client.post(self.list_url, {
            "name": "Christmas 1999",
            "valid_until": make_aware(datetime(1999, 12, 30)), # ----------> DATE IS INVALID
            "code": "NEWYEAR777",
            "discount": 50
        },
        format="json")

        self.assertEqual(response.status_code, 400)
