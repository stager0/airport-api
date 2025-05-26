from http.client import responses

from django.db.models import Count, F, Q
from django.db.models.functions import Length
from django.db.transaction import mark_for_rollback_on_error
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse, OpenApiExample
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

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
                name="name", description="Filter orders by MealOption Name (Chicken Curry etc.)",
                required=False, type=str
            ),
            OpenApiParameter(
                name="meal_type", description="Filter orders by Meal Option Type Id",
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
                name="Meal Option List Filter Example",
                value=[
                    {"id": 2, "name": "Beef Steak", "meal_type": "1", "weight": 400, "price": "15.00"}
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
                    {"name": "Beef Steak BBQ", "meal_type": "1", "weight": 500, "price": "19.00"},
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


class AirportViewSet(viewsets.ModelViewSet):
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


class CrewViewSet(viewsets.ModelViewSet):
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


class AirplaneTypeViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = [IsAdminOrIsAuthenticatedReadOnly]


class AirplaneViewSet(viewsets.ModelViewSet):
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


class DiscountCouponViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = DiscountCoupon.objects.all()
    serializer_class = DiscountCouponSerializer
    permission_classes = [IsAdminOrIsAuthenticatedReadOnly, ]
