from django.contrib import admin

from airport.models import (
    AirplaneType,
    Airplane,
    SnacksAndDrinks,
    MealOption,
    ExtraEntertainmentAndComfort,
    DiscountCoupon,
    Ticket,
    Airport,
    Route,
    Crew,
    Flight,
    Order
)

admin.site.register(AirplaneType)
admin.site.register(Airplane)
admin.site.register(Airport)
admin.site.register(Crew)
admin.site.register(SnacksAndDrinks)
admin.site.register(MealOption)
admin.site.register(ExtraEntertainmentAndComfort)
admin.site.register(DiscountCoupon)

class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0
    readonly_fields = ("discount",)

    def get_queryset(self, request):
        return (
            super().get_queryset(request)
            .select_related(
                "flight",
                "flight__route",
                "flight__route__source",
                "flight__route__destination",
                "order",
                "meal_option",
                "discount_coupon"
            )
            .prefetch_related(
                "extra_entertainment_and_comfort",
                "snacks_and_drinks"
            )
        )


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_route_display",
        "airplane",
        "departure_time",
        "arrival_time",
        "get_crew",
        "price_economy",
        "price_business",
        "luggage_price_1_kg"
    )
    list_filter = (
        "route__source__name",
        "route__destination__name",
        "departure_time",
    )
    search_fields = (
        "route__source__name",
        "route__destination__name",
        "departure_time",
        "arrival_time",
        "price_economy"
        )
    ordering = ("-departure_time",)
    list_per_page = 20

    @admin.display(description="Crew")
    def get_crew(self, obj):
        return " ,".join(f"{person.first_name} {person.last_name}, {person.position}" for person in obj.crew.all())

    @admin.display(description="Route")
    def get_route_display(self, obj):
        source_name = obj.route.source.name
        source_city = obj.route.source.closest_big_city
        destination_name = obj.route.destination.name
        destination_city = obj.route.destination.closest_big_city
        return f"{source_name} ({source_city}) -> {destination_name} ({destination_city})"


    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            "route__source",
            "route__destination",
            "airplane",
        ).prefetch_related("crew")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "user", "total_price")
    list_filter = ("total_price", "created_at")
    search_fields = ("created_at",)
    ordering = ("-created_at", "-total_price")
    readonly_fields  = ("created_at",)
    list_per_page = 20
    inlines = [TicketInline,]

    def get_queryset(self, request):
        return (
            super().get_queryset(request)
            .select_related("user")
            .prefetch_related(
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
        )

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "row",
        "letter",
        "discount",
        "has_luggage",
        "luggage_weight",
        "flight",
        "order",
        "price",
        "meal_option",
        "get_extra_entertainment_and_comfort",
        "get_snacks_and_drinks",
        "is_business",
        "discount_coupon"
    )
    list_filter = (
        "has_luggage",
        "is_business",
        "discount_coupon__code"
    )
    search_fields = ("discount_coupon__code", "discount", "flight__route__source__name")
    ordering = ("-order__created_at",)
    readonly_fields = ("discount",)
    list_per_page = 20

    @admin.display(description="ExtraEntertainmentAndComfort")
    def get_extra_entertainment_and_comfort(self, obj):
        return " ,".join(f"{extra.name} ({extra.price}$)" for extra in obj.extra_entertainment_and_comfort.all())

    @admin.display(description="SnacksAndDrinks")
    def get_snacks_and_drinks(self, obj):
        return " ,".join(f"{snack.name} ({snack.price}$)" for snack in obj.snacks_and_drinks.all())

    def get_queryset(self, request):
        return (
            super().get_queryset(request)
            .select_related(
                "flight",
                "flight__route",
                "flight__route__source",
                "flight__route__destination",
                "order",
                "meal_option",
                "discount_coupon"
            )
            .prefetch_related(
                "extra_entertainment_and_comfort",
                "snacks_and_drinks"
            )
        )


@admin.register(Route)
class AdminRoute(admin.ModelAdmin):
    list_display = ("id", "source", "destination", "distance")
    list_filter = ("source", "destination")
    search_fields = ("source__closest_big_city",)
    ordering = ("distance",)
    list_per_page = 20

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("source", "destination")
