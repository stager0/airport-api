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
admin.site.register(Route)
admin.site.register(Crew)
admin.site.register(SnacksAndDrinks)
admin.site.register(MealOption)
admin.site.register(ExtraEntertainmentAndComfort)
admin.site.register(DiscountCoupon)

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = (
        "id", "route", "airplane",
        "departure_time", "arrival_time", "get_crew",
        "price_economy", "price_business", "luggage_price_1_kg"
    )
    list_filter = (
        "route__source__name",
        "route__destination__name",
        "departure_time",
        "price_business",
        "price_economy",
        "luggage_price_1_kg"
    )
    search_fields = (
        "route__source__name",
        "route__destination__name",
        "departure_time",
        "arrival_time",
        "price_economy"
        )
    ordering = ("-departure_time",)

    @admin.display(description="Crew")
    def get_crew(self, obj):
        return " ,".join(f"{person.first_name} {person.last_name}, {person.position}" for person in obj.crew.all())

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            "route__source", "route__destination", "airplane",
        ).prefetch_related("crew")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "user", "total_price")
    list_filter = ("total_price", "created_at")
    search_fields = ("total_price", "created_at")
    ordering = ("-created_at",)
    readonly_fields  = ("created_at",)

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
        "flight",
        "order",
        "price",
        "is_business",
        "discount_coupon__code"
    )
    search_fields = ("discount_coupon__code", "discount")
    ordering = ("-order__created_at",)
    readonly_fields = ("discount",)

    def get_extra_entertainment_and_comfort(self, obj):
        return " ,".join([f"{extra.name} ({extra.price}$)" for extra in obj.get_extra_entertainment_and_comfort.all()])

    def get_snacks_and_drinks(self, obj):
        return " ,".join([f"{snack.name} ({snack.price}$)" for snack in obj.snacks_and_drinks.all()])