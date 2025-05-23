from django.urls import path, include
from rest_framework import routers

from airport.views import (
    MealOptionViewSet,
    SnacksAndDrinksViewSet,
    ExtraEntertainmentAndComfortViewSet,
    AirportViewSet,
    CrewViewSet,
    AirplaneTypeViewSet,
    AirplaneViewSet,
    RouteViewSet,
    FlightViewSet,
    OrderViewSet
)

app_name = "airport"

router = routers.DefaultRouter()

router.register("meal_option", MealOptionViewSet)
router.register("snacks_and_drinks", SnacksAndDrinksViewSet)
router.register("extra_entertainment_and_comfort", ExtraEntertainmentAndComfortViewSet)
router.register("airport", AirportViewSet)
router.register("crew", CrewViewSet)
router.register("airplane_type", AirplaneTypeViewSet)
router.register("airplane", AirplaneViewSet)
router.register("route", RouteViewSet)
router.register("flight", FlightViewSet)
router.register("order", OrderViewSet)

urlpatterns=[path("", include(router.urls))]