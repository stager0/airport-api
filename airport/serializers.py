from decimal import Decimal, ROUND_HALF_UP
from django.utils import timezone

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
    Order,
    DiscountCoupon
)
from user.serializers import UserOnlyIdAndNameSerializer


class DiscountCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCoupon
        fields = ("id", "name", "valid_until", "code", "discount")


class DiscountOnlyValueAndNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCoupon
        fields = ("id", "name", "discount")


class MealOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealOption
        fields = ("id", "name", "meal_type", "weight", "price", "image")


class MealOptionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealOption
        fields = ("id", "image")


class SnacksAndDrinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = SnacksAndDrinks
        fields = ("id", "name", "price", "image")


class SnacksAndDrinksImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SnacksAndDrinks
        fields = ("id", "image")


class ExtraEntertainmentAndComfortSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraEntertainmentAndComfort
        fields = ("id", "name", "price", "image")


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city")


class AirportSourceAndDestinationOnlyCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("closest_big_city",)


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name", "position")


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("id", "name",)


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields =("id", "name", "rows", "letters_in_row", "airplane_type", "image")


class AirplaneWithAirplaneType(AirplaneSerializer):
    airplane_type = AirplaneTypeSerializer(read_only=True)


class AirplaneNameSerializer(AirplaneSerializer):
    class Meta:
        model = Airplane
        fields = ("name",)


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "distance", "source", "destination")


class RouteListSerializer(RouteSerializer):
    source = AirportSerializer(read_only=True)
    destination = AirportSerializer(read_only=True)


class RouteSourceDestinationNamesSerializer(serializers.ModelSerializer):
    source = AirportSourceAndDestinationOnlyCitySerializer(read_only=True)
    destination = AirportSourceAndDestinationOnlyCitySerializer(read_only=True)

    class Meta:
        model = Route
        fields = ("distance", "source", "destination")


class FlightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flight
        fields = (
            "id",
            "departure_time",
            "arrival_time",
            "route",
            "airplane",
            "crew",
            "price_economy",
            "price_business",
            "rows_economy_from",
            "luggage_price_1_kg"
        )


class FlightListSerializer(FlightSerializer):
    route = RouteSourceDestinationNamesSerializer(read_only=True)
    airplane = AirplaneNameSerializer(read_only=True)
    places_available = serializers.IntegerField(read_only=True)
    business_places_available = serializers.SerializerMethodField(read_only=True)
    economy_places_available = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Flight
        fields = (
            "id",
            "departure_time",
            "arrival_time",
            "route",
            "airplane",
            "places_available",
            "business_places_available",
            "economy_places_available"
        )

    def get_business_places_available(self, obj):
        return (obj.airplane.seats_in_row_count * obj.rows_economy_from) - obj.taken_business

    def get_economy_places_available(self, obj):
        return (obj.airplane.seats_in_row_count * (obj.airplane.rows - obj.rows_economy_from)) - obj.economy_taken


class FlightRetrieveSerializer(FlightSerializer):
    crew = CrewSerializer(many=True, read_only=True)
    route = RouteListSerializer(read_only=True)
    airplane = AirplaneWithAirplaneType(read_only=True)
    all_free_places = serializers.SerializerMethodField(read_only=True)

    class Meta(FlightSerializer.Meta):
        fields = FlightSerializer.Meta.fields + ("all_free_places", "luggage_price_1_kg", "crew")

    def get_all_free_places(self, obj):
        taken_seats_and_letters = set(obj.tickets.values_list("row", "letter"))
        rows = int(obj.airplane.rows)
        letters = list(obj.airplane.letters_in_row)
        list_of_free_seats = []
        list_of_free_business_seats = []

        for row in range(1, rows + 1):
            for letter in letters:
                if (row, letter) not in taken_seats_and_letters:
                    if row > obj.rows_economy_from:
                        list_of_free_seats.append({"row": row, "letter": letter})
                    elif row <= obj.rows_economy_from:
                        list_of_free_business_seats.append({"row": row, "letter": letter})
        return f"Economy: {list_of_free_seats}",  f"Business: {list_of_free_business_seats}"


class FlightForOrderSerializer(FlightRetrieveSerializer):
    class Meta(FlightRetrieveSerializer.Meta):
        fields = (
            "id",
            "departure_time",
            "arrival_time",
            "route",
            "airplane",
            "luggage_price_1_kg"
        )


class TicketSerializer(serializers.ModelSerializer):
    meal_option = serializers.PrimaryKeyRelatedField(queryset=MealOption.objects.all())
    extra_entertainment_and_comfort = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=ExtraEntertainmentAndComfort.objects.all(),
        required=False,
        allow_empty=True
    )
    snacks_and_drinks = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=SnacksAndDrinks.objects.all(),
        required=False,
        allow_empty=True
    )
    discount_coupon = serializers.CharField(required=False)
    discount = serializers.IntegerField(read_only=True)

    def validate(self, attrs):
        Ticket.validate_ticket(
            row=attrs["row"],
            letter=attrs["letter"],
            airplane=attrs["flight"].airplane,
            error_to_raise=ValidationError
        )
        return attrs

    class Meta:
        model = Ticket
        fields = (
            "id",
            "row",
            "letter",
            "discount",
            "has_luggage",
            "flight",
            "order",
            "meal_option",
            "extra_entertainment_and_comfort",
            "snacks_and_drinks",
            "discount_coupon",
            "luggage_weight"
        )


class TicketDetailSerializer (serializers.ModelSerializer):
    flight = FlightForOrderSerializer(read_only=True)
    meal_option = MealOptionSerializer(read_only=True)
    extra_entertainment_and_comfort = ExtraEntertainmentAndComfortSerializer(many=True, read_only=True)
    snacks_and_drinks = SnacksAndDrinksSerializer(many=True, read_only=True)
    discount_coupon = DiscountOnlyValueAndNameSerializer(read_only=True)
    ticket_price = serializers.SerializerMethodField(read_only=True)
    luggage_price = serializers.SerializerMethodField(read_only=True)
    extra_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Ticket
        fields = (
            "id",
            "row",
            "letter",
            "discount",
            "has_luggage",
            "flight",
            "meal_option",
            "extra_entertainment_and_comfort",
            "snacks_and_drinks",
            "discount_coupon",
            "luggage_weight",
            "ticket_price",
            "luggage_price",
            "extra_price"
        )

    def get_ticket_price(self, obj):
        if obj.is_business is True:
            return Flight.objects.get(id=obj.flight.id).price_business
        return Flight.objects.get(id=obj.flight.id).price_economy

    def get_luggage_price(self, obj):
        if obj.has_luggage and obj.luggage_weight is not None:
            return obj.luggage_weight * obj.flight.luggage_price_1_kg

    def get_extra_price(self, obj):
        entertainment = [item.name for item in obj.extra_entertainment_and_comfort.all()]
        snacks = [item.name for item in obj.snacks_and_drinks.all()]
        meal_type = obj.meal_option.name

        total_price = 0
        if len(entertainment) > 0:
            for i in entertainment:
                total_price += ExtraEntertainmentAndComfort.objects.get(name=i).price
        if len(snacks) > 0:
            for i in snacks:
                total_price += SnacksAndDrinks.objects.get(name=i).price

        if meal_type and meal_type != "NONE":
            total_price += MealOption.objects.get(name=meal_type).price

        return total_price


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "created_at", "tickets")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            total_price = 0

            for ticket_data in tickets_data:
                extras = ticket_data.pop("extra_entertainment_and_comfort", [])
                snacks_drinks = ticket_data.pop("snacks_and_drinks", [])
                meal_option = ticket_data.pop("meal_option")
                discount_coupon = ticket_data.pop("discount_coupon", None)
                coupon_object = None
                if discount_coupon:
                    try:
                        coupon_object = DiscountCoupon.objects.get(code=discount_coupon)
                    except DiscountCoupon.DoesNotExist:
                        pass

                if coupon_object and coupon_object.valid_until > timezone.now():
                    ticket = Ticket.objects.create(order=order, meal_option=meal_option, discount_coupon=coupon_object, **ticket_data)
                else:
                    ticket = Ticket.objects.create(order=order, meal_option=meal_option, **ticket_data)

                ticket.extra_entertainment_and_comfort.set(extras)
                ticket.snacks_and_drinks.set(snacks_drinks)

                ticket_price = 0
                if ticket.flight:
                    if ticket.is_business:
                        ticket_price += ticket.flight.price_business
                    else:
                        ticket_price += ticket.flight.price_economy

                if ticket.meal_option:
                    ticket_price += ticket.meal_option.price

                if ticket.has_luggage is False and ticket.luggage_weight is not None:
                    ticket.has_luggage = True

                if ticket.has_luggage and ticket.luggage_weight is not None:
                    ticket_price += Decimal(ticket.luggage_weight) * ticket.flight.luggage_price_1_kg

                for extra in extras:
                    ticket_price += extra.price

                for snack in snacks_drinks:
                    ticket_price += snack.price

                if coupon_object and coupon_object.valid_until > timezone.now():
                    discount = coupon_object.discount
                    ticket_price *= Decimal(1 - discount / 100)
                    ticket.discount = discount

                if not coupon_object or ticket.discount <= 0 or coupon_object.valid_until < timezone.now():
                    ticket.discount = 0
                    ticket.discount_coupon = None

                total_price += ticket_price
                ticket.price = Decimal(total_price).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                ticket.save()

            order.total_price = Decimal(total_price).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            order.save()
            return order


class OrderListSerializer(OrderSerializer):
    count_of_tickets = serializers.IntegerField(read_only=True)
    source = serializers.CharField(read_only=True)
    destination = serializers.CharField(read_only=True)
    user = UserOnlyIdAndNameSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ("id", "created_at", "total_price", "user", "count_of_tickets", "source", "destination")


class OrderRetrieveSerializer(serializers.ModelSerializer):
    tickets = TicketDetailSerializer(many=True, read_only=True)
    user = UserOnlyIdAndNameSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ("id", "created_at", "total_price", "user", "tickets")
        read_only_fields = ("user",)
