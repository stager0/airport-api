from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from airport.models import MealOption, SnacksAndDrinks
from airport.serializers import (
    MealOptionSerializer,
    SnacksAndDrinksSerializer,
)


class MealOptionViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = MealOption.objects.all()
    serializer_class = MealOptionSerializer


class SnacksAndDrinksViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = SnacksAndDrinks.objects.all()
    serializer_class = SnacksAndDrinksSerializer
