from rest_framework import serializers

from airport.models import MealOption, SnacksAndDrinks


class MealOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealOption
        fields = ("name", "meal_type", "weight", "price")


class SnacksAndDrinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = SnacksAndDrinks
        fields = ("name", "price")
