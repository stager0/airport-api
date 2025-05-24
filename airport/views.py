from django.db.models import Count, F
from django.template.context_processors import request
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
    Order
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
)


class MealOptionViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = MealOption.objects.all()
    serializer_class = MealOptionSerializer
    permission_classes = [IsAdminOrIsAuthenticatedReadOnly]


class SnacksAndDrinksViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = SnacksAndDrinks.objects.all()
    serializer_class = SnacksAndDrinksSerializer
    permission_classes = [IsAdminOrIsAuthenticatedReadOnly]


class ExtraEntertainmentAndComfortViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = ExtraEntertainmentAndComfort.objects.all()
    serializer_class = ExtraEntertainmentAndComfortSerializer
    permission_classes = [IsAdminOrIsAuthenticatedReadOnly]


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsAdminOrIsAuthenticatedReadOnly]


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = [IsAdminOrIsAuthenticatedReadOnly]


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


class FlightViewSet(viewsets.ModelViewSet):
    queryset = (Flight.objects.select_related(
        "airplane",
        "route",
        "route__source",
        "route__destination",
        "airplane__airplane_type"
    ))

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
        if destination or airplane or date or source:
            if destination:
                queryset = queryset.filter(route__destination__closest_big_city__icontains=destination)
            if source:
                queryset = queryset.filter(route__source__closest_big_city__icontains=source)
            if airplane:
                queryset = queryset.filter(airplane__name__icontains=airplane)
            if date:
                queryset = queryset.filter(departure_time_gte=date)
            return queryset.distinct()

        if self.action == "list":
            return queryset
        elif self.action == "retrieve":
            return queryset.prefetch_related("crew__flights")


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Order.objects.all().annotate(
        count_of_tickets=Count(
        "tickets"
    ), source=F(
        "tickets__flight__route__source__closest_big_city"
    ), destination=F(
        "tickets__flight__route__destination__closest_big_city"
    ))
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
