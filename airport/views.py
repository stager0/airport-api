from django.db.models import Count, F, Q
from django.db.models.functions import Length
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
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
from airport.schema.airplane_schema import airplane_schema
from airport.schema.airplane_type_schema import airport_type_schema
from airport.schema.airport_schema import airport_schema
from airport.schema.crew_schema import crew_schema
from airport.schema.discount_coupon_schema import discount_coupon_schema
from airport.schema.extra_entertainment_and_comfort_schema import extra_entertainment_and_comfort_schema
from airport.schema.flight_schema import flight_schema
from airport.schema.meal_option_schema import meal_option_schema
from airport.schema.order_schema import order_schema
from airport.schema.route_schema import route_schema
from airport.schema.snacks_and_drinks_schema import snacks_and_drinks_schema
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
    OrderSerializer,
    RouteListSerializer,
    FlightListSerializer,
    FlightRetrieveSerializer,
    OrderListSerializer,
    OrderRetrieveSerializer,
    DiscountCouponSerializer,
    MealOptionImageSerializer,
    SnacksAndDrinksImageSerializer,
    CrewImageSerializer,
)


class UploadImageMixin:
    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=[IsAdminUser]
    )
    def upload_image(self, request, pk=None):
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@meal_option_schema
class MealOptionViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
    UploadImageMixin
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

    def get_serializer_class(self):
        if self.action == "upload_image":
            return MealOptionImageSerializer
        return MealOptionSerializer


@snacks_and_drinks_schema
class SnacksAndDrinksViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
    UploadImageMixin
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

    def get_serializer_class(self):
        if self.action == "upload_image":
            return SnacksAndDrinksImageSerializer
        return SnacksAndDrinksSerializer


@extra_entertainment_and_comfort_schema
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


@airport_schema
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


@crew_schema
class CrewViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
    UploadImageMixin
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

    def get_serializer_class(self):
        if self.action == "upload_image":
            return CrewImageSerializer
        return CrewSerializer


@airport_type_schema
class AirplaneTypeViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = [IsAdminOrIsAuthenticatedReadOnly]


@airplane_schema
class AirplaneViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    permission_classes = [IsAdminOrIsAuthenticatedReadOnly]


@route_schema
class RouteViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
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


@flight_schema
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
        date_from = self.request.query_params.get("departure_time_from")
        date_to = self.request.query_params.get("departure_time_to")
        arrival_time = self.request.query_params.get("arrival_time")

        queryset = self.queryset
        if destination:
            queryset = queryset.filter(route__destination__closest_big_city__icontains=destination)
        if source:
            queryset = queryset.filter(route__source__closest_big_city__icontains=source)
        if airplane:
            queryset = queryset.filter(airplane__name__icontains=airplane)
        if date_from:
            queryset = queryset.filter(departure_time__gte=date_from)
        if date_to:
            queryset = queryset.filter(departure_time__lte=date_to)
        if arrival_time:
            queryset = queryset.filter(arrival_time__gte=arrival_time)

        if self.action == "list":
            return queryset.prefetch_related("tickets").distinct().annotate(
                row_length=Length("airplane__letters_in_row"),
                places_available=(F("airplane__rows") * F("row_length")) - Count("tickets"),
                taken_business=Count("tickets", filter=Q(tickets__is_business=True), distinct=True),
                economy_taken=Count("tickets", filter=Q(tickets__is_business=False), distinct=True)
            )

        return queryset.prefetch_related("crew__flights").distinct()


@order_schema
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

        if self.action == "list":
            return queryset.prefetch_related(
                "tickets",
                "tickets__flight",
                "tickets__flight__route",
                "tickets__flight__route__source",
                "tickets__flight__route__destination",
                "tickets__extra_entertainment_and_comfort",
                "tickets__snacks_and_drinks",
                "tickets__meal_option",
                "tickets__discount_coupon",
                "tickets__flight__airplane"
            )

        elif self.action == "retrieve":
            return queryset.prefetch_related(
                "tickets__flight__route__source",
                "tickets__flight__route__destination",
                "tickets__extra_entertainment_and_comfort",
                "tickets__snacks_and_drinks",
                "tickets__meal_option",
                "tickets__discount_coupon",
                "tickets__flight__airplane"
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


@discount_coupon_schema
class DiscountCouponViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = DiscountCoupon.objects.all()
    serializer_class = DiscountCouponSerializer
    permission_classes = [IsAdminOrIsAuthenticatedReadOnly, ]
