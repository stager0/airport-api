from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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
    Ticket,
    Order
)


class MealOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealOption
        fields = ("name", "meal_type", "weight", "price")


class SnacksAndDrinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = SnacksAndDrinks
        fields = ("name", "price")


class ExtraEntertainmentAndComfortSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraEntertainmentAndComfort
        fields = ("name", "price")


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("name", "closest_big_city")


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("first_name", "last_name", "position")


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("name",)


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields =("name", "rows", "letters_in_row", "airplane_type")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("distance", "source", "destination")


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = (
            "departure_time",
            "arrival_time",
            "route",
            "airplane",
            "crew"
        )


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs)
        Ticket.validate_ticket(
            row=attrs["row"],
            letter=attrs["letter"],
            airplane=attrs["flight"].airplane,
            error_to_raise=ValidationError
        )
        return data

    class Meta:
        model = Ticket
        fields = (
            "row",
            "letter",
            "discount",
            "has_luggage",
            "flight",
            "order",
            "price",
            "meal_option",
            "extra_entertainment_and_comfort",
            "snacks_and_drinks"
        )

class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("created_at", "total_price", "user", "tickets")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket in tickets_data:
                Ticket.objects.create(order=order, **ticket)
            return order
