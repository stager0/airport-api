from django.db.models import Count, F, Q
from django.db.models.functions import Length
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse, OpenApiExample
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from airport.example_swagger_dicts.dict_order_retrieve_example import example_order_retrieve_dict
from airport.models import (
    MealOption,
    SnacksAndDrinks,
    ExtraEntertainmentAndComfort,
    Airport,
    Crew,
    AirplaneType,
    Airplane,
    Route,
    Flight,
    Order, DiscountCoupon
)
from airport.permissions import IsAdminOrIsAuthenticatedReadOnly
from airport.serializers import (
    MealOptionSerializer,
    SnacksAndDrinksSerializer,
    ExtraEntertainmentAndComfortSerializer,
    AirportSerializer,
    CrewSerializer,
    AirplaneTypeSerializer,
    AirplaneSerializer,
    RouteSerializer,
    FlightSerializer,
    OrderSerializer, RouteListSerializer, FlightListSerializer, FlightRetrieveSerializer, OrderListSerializer,
    OrderRetrieveSerializer, DiscountCouponSerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary="Retrieve a list of all Meal Options",
        description="Returns a list of all Meal Options available in the system",
        tags=["MealOption"],
        parameters=[
            OpenApiParameter(
                name="name", description="Filter by MealOption Name (Chicken Curry etc.)",
                required=False, type=str
            ),
            OpenApiParameter(
                name="meal_type", description="Filter by Meal Option Type Id",
                required=False, type=int
            ),
            OpenApiParameter(
                name="price",
                description="Filter to this price (if ?price=20 -> return all Meal Option which cost less than 20 )",
                required=False, type=int
            )
        ],
        responses={
            200: MealOptionSerializer(many=True),
            401: OpenApiResponse(description="Authentication credentials were not provided")
        },
        examples=[
            OpenApiExample(
                name="Meal Option List Example",
                value=[
                    {"id": 2, "name": "Beef Steak", "meal_type": "1", "weight": 400, "price": 15.00}
                ],
                response_only=True
            )
        ]
    ),
    create=extend_schema(
        summary="Create a new Meal Option",
        description="Creates a new Meal Option with provided data (name, meal_type, weight, price)",
        tags=["MealOption"],
        request=MealOptionSerializer,
        responses={
            201: MealOptionSerializer,
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            400: OpenApiResponse(
                description="Bad request",
                examples=[
                    OpenApiExample(
                        "Incorrect price and empty name",
                        value={
                            "name": ["This field may not be blank."],
                            "price": ["A valid number is required."]
                        },
                        status_codes=["400"]
                    )
                ]
            ),
        },
        examples=[
            OpenApiExample(
                name="Create Meal Type Example",
                value=[
                    {"name": "Beef Steak BBQ", "meal_type": "1", "weight": 500, "price": 19.00},
                ],
                request_only=True
            )
        ]
    ),
)
class MealOptionViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = MealOption.objects.all()
    serializer_class = MealOptionSerializer
    permission_classes = [IsAdminOrIsAuthenticatedReadOnly]

    def get_queryset(self):
        price = self.request.query_params.get("price")
        name = self.request.query_params.get("name")
        meal_type = self.request.query_params.get("meal_type")

        queryset = self.queryset
        if price:
            queryset = queryset.filter(price__lte=price)
        if name:
            queryset = queryset.filter(name__icontains=name)
        if meal_type:
            queryset = queryset.filter(meal_type=meal_type)

        return queryset.distinct()


@extend_schema_view(
    list=extend_schema(
        summary="Get a list of all Snacks and Drinks",
        description="Returns a list of all Snacks and Drinks available in the system",
        tags=["snacks_and_drinks"],
        request=SnacksAndDrinksSerializer,
        parameters=[
            OpenApiParameter(
                name="name", description="Filter by Name (water, cola, fanta etc.)",
                required=False, type=str
            )
        ],
        responses={
            200: SnacksAndDrinksSerializer(many=True),
            401: OpenApiResponse(description="Authentication credentials were not provided"),
        },
        examples=[
            OpenApiExample(
                name="Snacks And Drinks List Example",
                value=[
                    {
                        "id": 1,
                        "name": "Coca-Cola 0.5",
                        "price": 2.00
                    },
                    {
                        "id": 2,
                        "name": "Fanta 0.5",
                        "price": 2.00
                    },
                ],
                response_only=True
            )
        ]
    ),
    create=extend_schema(
        summary="Create a new Snack Or Drink",
        description="Creates a new Snack or Drink with provided data (name, price)",
        tags=["snacks_and_drinks"],
        request=SnacksAndDrinksSerializer,
        responses={
            201: SnacksAndDrinksSerializer,
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            400: OpenApiResponse(
                description="Bad request",
                examples=[
                    OpenApiExample(
                        "Empty (incorrect) name and price",
                        value={
                            "name": ["This field may not be blank."],
                            "price": ["A valid number is required."],
                        },
                        status_codes=[400]
                    )
                ]
            )
        },
        examples=[
            OpenApiExample(
                "Create example",
                value={"name": "Tee", "price": 1.99},
                request_only=True
            )
        ]
    )
)
class SnacksAndDrinksViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = SnacksAndDrinks.objects.all()
    serializer_class = SnacksAndDrinksSerializer
    permission_classes = [IsAdminOrIsAuthenticatedReadOnly]

    def get_queryset(self):
        name = self.request.query_params.get("name")

        queryset = self.queryset
        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset.distinct()


@extend_schema_view(
    list=extend_schema(
        summary="Get all from Extra Entertainment and Comfort",
        description="Retrieve a list with all Extra Entertainment and Comfort items",
        tags=["extra_entertainment_and_comfort"],
        request=ExtraEntertainmentAndComfortSerializer,
        parameters=[
            OpenApiParameter(
                name="name", description="Filter by item name (tablet, pillow etc.)",
                required=False, type=str
            )
        ],
        responses={
            200: ExtraEntertainmentAndComfortSerializer(many=True),
            401: OpenApiResponse(description="Authentication credentials were not provided")
        },
        examples=[
            OpenApiExample(
                "List Example",
                value=[
                    {"id": 1, "name": "Tablet with movies/games", "price": "9.99"},
                ],
                response_only=True
            )
        ]
    ),
    create=extend_schema(
        summary="Create a new Extra Entertainment and Comfort item",
        description="Create a new item Extra Entertainment and Comfort by provided data (name, price)",
        request=ExtraEntertainmentAndComfortSerializer,
        tags=["extra_entertainment_and_comfort"],
        responses={
            201: ExtraEntertainmentAndComfortSerializer,
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            400: OpenApiResponse(
                description="Bad request",
                examples=[
                    OpenApiExample(
                        "Empty (incorrect) Name and Price",
                        value={
                            "name": ["This field may not be blank."],
                            "price": ["A valid number is required."]
                        },
                        status_codes=[400]
                    ),
                ]
            )
        },
        examples=[
            OpenApiExample(
                "Create Example",
                value={
                    "name": "Tablet",
                    "price": 17.50
                },
                request_only=True
            )
        ]
    )
)
class ExtraEntertainmentAndComfortViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = ExtraEntertainmentAndComfort.objects.all()
    serializer_class = ExtraEntertainmentAndComfortSerializer
    permission_classes = [IsAdminOrIsAuthenticatedReadOnly]

    def get_queryset(self):
        name = self.request.query_params.get("name")

        queryset = self.queryset
        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset.distinct()


@extend_schema_view(
    list=extend_schema(
        summary="Get a list of Airports",
        description="Retrieve a list of all available Airports (from which this company flies)",
        tags=["airport"],
        request=AirportSerializer,
        responses={
            200: AirportSerializer(many=True),
            401: OpenApiResponse(description="Authentication credentials were not provided")
        },
        parameters=[
            OpenApiParameter(
                name="closest_big_city", description="Filter by closest_big_city",
                required=False, type=str
            ),
            OpenApiParameter(
                name="airport_name", description="Filter by airport_name",
                required=False, type=str
            )
        ],
        examples=[
            OpenApiExample(
                "List Example",
                value={
                    "id": 1,
                    "name": "JFK International Airport",
                    "closest_big_city": "New York City"
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create an Airport",
        description="Create an Airport with provided data (name (airport name), closest big city)",
        tags=["airport"],
        request=AirportSerializer,
        responses={
            201: AirportSerializer,
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            400: OpenApiResponse(
                description="Bad Request",
                examples=[
                    OpenApiExample(
                        "Empty name and closest_big_city",
                        value={
                            "name": ["This field may not be blank."],
                            "closest_big_city": ["This field may not be blank."]
                        },
                        status_codes=[400]
                    )
                ]
            )
        },
        examples=[
            OpenApiExample(
                "Create new Airport",
                value={
                    "name": "Airport Boryspil, Kiev",
                    "closest_big_city": "Kiev"
                },
                request_only=True
            )
        ]
    )
)
class AirportViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsAdminOrIsAuthenticatedReadOnly]

    def get_queryset(self):
        closest_big_city = self.request.query_params.get("closest_big_city")
        airport_name = self.request.query_params.get("name")

        queryset = self.queryset
        if closest_big_city:
            queryset = queryset.filter(closest_big_city__icontains=closest_big_city)
        if airport_name:
            queryset = queryset.filter(name__icontains=airport_name)

        return queryset.distinct()


@extend_schema_view(
    list=extend_schema(
        summary="Get a list of all Crews(workers)",
        description="Retrieve a list of all actual Crews in format (first_name, last_name, position)",
        tags=["crew"],
        request=CrewSerializer,
        responses={
            200: CrewSerializer(many=True),
            401: OpenApiResponse(description="Authentication credentials were not provided")
        },
        parameters=[
            OpenApiParameter(
                name="first_name", description="Filter by first_name",
                required=False, type=str
            ),
            OpenApiParameter(
                name="last_name", description="Filter by last_name",
                required=False, type=str
            ),
            OpenApiParameter(
                name="position", description="Filter by position",
                required=False, type=str
            )
        ],
        examples=[
            OpenApiExample(
                "Item from Crew List Example",
                value={
                    "id": 1,
                    "first_name": "James",
                    "last_name": "Kirk",
                    "position": "CAPTAIN"
                },
            )
        ]
    ),
    create=extend_schema(
        summary="Create a Crew Person",
        description="Creates a crew Person with provided data (first_name, last_name, position)",
        tags=["crew"],
        request=CrewSerializer,
        responses={
            201: CrewSerializer,
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            400: OpenApiResponse(
                description="Bad Request",
                examples=[
                    OpenApiExample(
                        "Empty first_name and last_name",
                        value={
                            "first_name": ["This field may not be blank."],
                            "last_name": ["This field may not be blank."]
                        },
                        status_codes=[400]
                    )
                ]
            )
        },
        examples=[
            OpenApiExample(
                "Create new Crew Person",
                value={
                    "first_name": "John",
                    "last_name": "Muller",
                    "position": "CAPTAIN"
                },
                request_only=True
            )
        ]
    )
)
class CrewViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = [IsAdminOrIsAuthenticatedReadOnly]

    def get_queryset(self):
        first_name = self.request.query_params.get("first_name")
        last_name = self.request.query_params.get("last_name")
        position = self.request.query_params.get("position")

        queryset = self.queryset
        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)
        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)
        if position:
            queryset = queryset.filter(position__icontains=position)

        return queryset.distinct()


@extend_schema_view(
    list=extend_schema(
        summary="Get a list of all Airplane Types",
        description="Retrieve a list of all Airplane Types (owned by the company)",
        tags=["airplane_type"],
        request=AirplaneTypeSerializer,
        responses={
            200: AirplaneTypeSerializer(many=True),
            401: OpenApiResponse(description="Authentication credentials were not provided")
        },
        examples=[
            OpenApiExample(
                "Item from AirplaneType List Example",
                value={
                    "id": 1,
                    "name": "Boeing 777"
                },
            )
        ]
    ),
    create=extend_schema(
        summary="Create an Airplane Type",
        description="Creates an Airplane Type with provided name",
        tags=["airplane_type"],
        request=AirplaneType,
        responses={
            201: AirplaneType,
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            400: OpenApiResponse(
                description="Bad Request",
                examples=[
                    OpenApiExample(
                        "Empty Airplane Name",
                        value={
                            "name": ["This field may not be blank."]
                        },
                        status_codes=[400]
                    )
                ]
            )
        },
        examples=[
            OpenApiExample(
                "Create new Airplane Type",
                value={
                    "name": "Boeing",
                },
                request_only=True
            )
        ]
    ),
)
class AirplaneTypeViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = [IsAdminOrIsAuthenticatedReadOnly]


@extend_schema_view(
    list=extend_schema(
        summary="Get a list of all Airplanes",
        description="Retrieve a list of all Airplanes in format (name, rows, letters_in_row, airplane_type)",
        tags=["airplane"],
        request=AirplaneSerializer,
        responses={
            200: AirplaneSerializer(many=True),
            401: OpenApiResponse(description="Authentication credentials were not provided")
        },
        examples=[
            OpenApiExample(
                "Item from Airplane List Example",
                value={
                    "id": 1,
                    "name": "Sky Explorer",
                    "rows": 30,
                    "letters_in_row": "ABCDEF",
                    "airplane_type": 1
                },
            )
        ]
    ),
    create=extend_schema(
        summary="Create an Airplane",
        description="Creates an Airplane with provided data (name, rows, letters_in_row, airplane_type(pk))",
        tags=["airplane"],
        request=AirplaneSerializer,
        responses={
            201: AirplaneSerializer,
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            400: OpenApiResponse(
                description="Bad Request",
                examples=[
                    OpenApiExample(
                        "Empty name, rows, letters_on_row, airplane_type",
                        value={
                            "name": ["This field may not be blank."],
                            "rows": ["A valid integer is required."],
                            "letters_in_row": ["This field may not be blank."],
                            "airplane_type": ["This field may not be null."]
                        },
                        status_codes=[400]
                    )
                ]
            )
        },
        examples=[
            OpenApiExample(
                "Create a new Airplane",
                value={
                    "name": "Sky Explorer Turbo",
                    "rows": 25,
                    "letters_in_row": "ABCDE",
                    "airplane_type": 1
                },
                request_only=True
            )
        ]
    )
)
class AirplaneViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    permission_classes = [IsAdminOrIsAuthenticatedReadOnly]


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related("source", "destination")
    serializer_class = RouteSerializer
    permission_classes = [IsAdminOrIsAuthenticatedReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        return RouteSerializer

    def get_queryset(self):
        source = self.request.query_params.get("source")
        destination = self.request.query_params.get("destination")
        source_airport = self.request.query_params.get("source_airport")
        destination_airport = self.request.query_params.get("destination_airport")

        queryset = self.queryset
        if source:
            queryset = queryset.filter(source__closest_big_city__icontains=source)
        elif destination:
            queryset = queryset.filter(destination__closest_big_city__icontains=destination)
        elif source_airport:
            queryset = queryset.filter(source__name__icontains=source_airport)
        elif destination_airport:
            queryset = queryset.filter(destination__name__icontains=destination_airport)

        return queryset.distinct()


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.select_related(
        "airplane",
        "route",
        "route__source",
        "route__destination",
        "airplane__airplane_type",
    )

    serializer_class = FlightSerializer
    permission_classes = [IsAdminOrIsAuthenticatedReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        elif self.action == "retrieve":
            return FlightRetrieveSerializer
        return FlightSerializer

    def get_queryset(self):
        destination = self.request.query_params.get("destination")
        source = self.request.query_params.get("source")
        airplane = self.request.query_params.get("airplane")
        date = self.request.query_params.get("departure_time")

        queryset = self.queryset
        if destination:
            queryset = queryset.filter(route__destination__closest_big_city__icontains=destination)
        if source:
            queryset = queryset.filter(route__source__closest_big_city__icontains=source)
        if airplane:
            queryset = queryset.filter(airplane__name__icontains=airplane)
        if date:
            queryset = queryset.filter(departure_time_gte=date)

        if self.action == "list":
            return queryset.prefetch_related("tickets").distinct().annotate(
                row_length=Length("airplane__letters_in_row"),
                places_available=(F("airplane__rows") * F("row_length")) - Count("tickets"),
                taken_business=Count("tickets", filter=Q(tickets__is_business=True), distinct=True),
                economy_taken=Count("tickets", filter=Q(tickets__is_business=False), distinct=True)
            )

        elif self.action == "retrieve":
            return queryset.prefetch_related("crew__flights").distinct()


@extend_schema_view(
    list=extend_schema(
        summary="Get all Orders (only for actual user)",
        description="Retrieve list of all Orders for actual(request) user. User can see only personal orders",
        tags=["order"],
        responses={
            200: OrderListSerializer,
            401: OpenApiResponse(description="Authorisation credentials were not provided"),
        },
        request=OrderListSerializer,
        examples=[
            OpenApiExample(
                "Item from Orders List, Example",
                value={
                    "id": 33,
                    "created_at": "2025-05-26T12:01:25.173735Z",
                    "total_price": "685.48",
                    "user": {
                        "id": 1,
                        "username": "admin"
                    },
                    "count_of_tickets": 1,
                    "source": "New York City",
                    "destination": "London"
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create an Order",
        description="Creates an Order and tickets, it counts order.total_price and etc. It's need only to add all tickets",
        request=OrderSerializer,
        tags=["order"],
        responses={
            201: OrderSerializer,
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            400: OpenApiResponse(
                description="Bad Request",
                examples=[
                    OpenApiExample(
                        "No Ticket",
                        value={
                            "tickets": {
                                "non_field_errors": [
                                    "This list may not be empty."
                                ]
                            }
                        },
                        status_codes=[400]
                    )
                ]
            )
        },
        examples=[
            OpenApiExample(
                "Create new Order Example",
                value=[
                    {
                        "tickets": [
                            {
                                "row": 12,
                                "letter": "C",
                                "has_luggage": "true",
                                "flight": 1,
                                "meal_option": 6,
                                "extra_entertainment_and_comfort": "[1, 2, 3, 4, 5]",
                                "snacks_and_drinks": "[6, 1, 2, 3, 4, 5]",
                                "luggage_weight": 49.0
                            }
                        ],
                    }
                ],
                request_only=True
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Get Single Item by Id",
        description="Retrieve detail information about an order (all info about tickets, prices and etc.) using its unique ID",
        tags=["order"],
        request=OrderRetrieveSerializer,
        responses={
            200: OrderRetrieveSerializer,
            404: OpenApiResponse(description="No Order matches the given query.")
        },
        examples=[
            OpenApiExample(
                "Retrieve Example",
                value=[
                    example_order_retrieve_dict
                ]
            )
        ]
    )
)
class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    queryset = Order.objects.all().annotate(
        count_of_tickets=Count(
            "tickets"
        ), source=F(
            "tickets__flight__route__source__closest_big_city"
        ), destination=F(
            "tickets__flight__route__destination__closest_big_city"
        )).select_related("user")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        if self.action == "retrieve":
            return queryset.prefetch_related(
                "tickets__flight__route__source",
                "tickets__flight__route__destination",
                "tickets__extra_entertainment_and_comfort",
                "tickets__snacks_and_drinks",
                "tickets__meal_option"
            )
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderRetrieveSerializer
        if self.action == "list":
            return OrderListSerializer
        if self.action == "create":
            return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema_view(
    list=extend_schema(
        summary="Get a list of all Discount Coupons",
        description="Retrieve a list of all Discount Coupons in format (name, valid_until, code, discount)",
        tags=["discount_coupon"],
        request=DiscountCouponSerializer,
        responses={
            200: DiscountCouponSerializer(many=True),
            401: OpenApiResponse(description="Authentication credentials were not provided")
        },
        examples=[
            OpenApiExample(
                "Item from Airplane List Example",
                value={
                    "id": 4,
                    "name": "Expired Deal",
                    "valid_until": "2024-12-31T23:59:59Z",
                    "code": "OLD111DEAL",
                    "discount": 20
                },
            )
        ]
    ),
    create=extend_schema(
        summary="Create an Discount Coupon",
        description="Create an Discount Coupon with provided data (name, valid_until, code, discount (0-100))",
        tags=["discount_coupon"],
        request=DiscountCouponSerializer,
        responses={
            201: DiscountCouponSerializer,
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            400: OpenApiResponse(
                description="Bad Request",
                examples=[
                    OpenApiExample(
                        "Empty name, valid_until, code, discount",
                        value={
                            "name": ["This field may not be blank."],
                            "valid_until": ["Datetime has wrong format. Use one of these formats instead: "
                                            "YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]."],
                            "code": ["This field may not be blank."],
                            "discount": ["A valid integer is required."]
                        },
                        status_codes=[400]
                    )
                ]
            )
        },
        examples=[
            OpenApiExample(
                "Create a new Discount Coupon",
                value={
                    "name": "New year BOOM",
                    "valid_until": "2024-12-31T23:59:59Z",
                    "code": "NEWYEAR111",
                    "discount": 25
                },
                request_only=True
            )
        ]
    )
)
class DiscountCouponViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = DiscountCoupon.objects.all()
    serializer_class = DiscountCouponSerializer
    permission_classes = [IsAdminOrIsAuthenticatedReadOnly, ]
