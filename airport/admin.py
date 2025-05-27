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
admin.site.register(Order)
admin.site.register(SnacksAndDrinks)
admin.site.register(MealOption)
admin.site.register(ExtraEntertainmentAndComfort)
admin.site.register(DiscountCoupon)
admin.site.register(Ticket)

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = (
        "id", "route", "airplane",
        "departure_time", "arrival_time", "crew",
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

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "user", "total_price")
    list_filter = ("total_price", "created_at")
    search_fields = ("total_price", "created_at")
    ordering = ("-created_at",)
    readonly_fields  = ("created_at",)
