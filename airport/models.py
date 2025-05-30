import os.path
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify

from airport.validators import validate_discount_coupon_code, validate_discount_date


def create_custom_uuid_ticket():
    return str(uuid.uuid4())[:23]  # example: f47ac10b-58cc-4372-a567

def create_custom_path(instance, filename):
    _, extension = os.path.splitext(filename)
    model_lower = str(instance.__class__.__name__).lower() + "s_media_files"
    slug = str(instance)[:50]
    return os.path.join(
        f"uploads/{model_lower}/",
        f"{slugify(slug)}-{uuid.uuid4()}{extension}"
    )


class AirplaneType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.name)


class Airplane(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField(validators=[MaxValueValidator(200)])
    letters_in_row = models.CharField(max_length=15)
    airplane_type = models.ForeignKey(
        AirplaneType,
        on_delete=models.CASCADE,
        related_name="airplanes",
    )
    image = models.ImageField(null=True, blank=True, upload_to=create_custom_path)

    @property
    def capacity(self) -> int:
        return len(self.letters_in_row) * self.rows

    @property
    def list_of_seats(self):
        return [i for i in self.letters_in_row]

    @property
    def seats_in_row_count(self):
        cleaned_letters_in_row = self.letters_in_row.replace(" ", "")
        return len(cleaned_letters_in_row)

    def __str__(self):
        return f"{self.name}, rows: {self.rows}, letters in row: {self.letters_in_row}"


class Airport(models.Model):
    name = models.CharField(max_length=255)
    closest_big_city = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}, city: ({self.closest_big_city})"


class Route(models.Model):
    source = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="departures"
    )
    destination = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="arrivals"
    )
    distance = models.IntegerField(validators=[MaxValueValidator(9999)])

    def __str__(self):
        return (f"Source: {self.source.name} ({self.source.closest_big_city}) "
                f"-> Destination: {self.destination.name} ({self.destination.closest_big_city})")


class Crew(models.Model):
    POSITIONS_CHOICES = [
        ("CAPTAIN", "Captain"),
        ("FIRST_OFFICER", "First Officer"),
        ("LEAD_FLIGHT_ATTENDANT", "Lead Flight Attendant"),
        ("FLIGHT_ATTENDANT", "Flight Attendant")
    ]
    first_name = models.CharField(max_length=125)
    last_name = models.CharField(max_length=125)
    position = models.CharField(max_length=50, choices=POSITIONS_CHOICES)
    image = models.ImageField(null=True, blank=True, upload_to=create_custom_path)

    def __str__(self):
        return (
            f"{self.first_name} "
            f"{self.last_name}, "
            f"Position: {self.get_position_display()}"
        )

    @property
    def full_name_and_position(self):
        return self.first_name + " " + self.last_name + ", Position: " + self.get_position_display()


class Flight(models.Model):
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="flights"
    )
    airplane = models.ForeignKey(
        Airplane,
        on_delete=models.CASCADE,
        related_name="flights",
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(
        Crew,
        related_name="flights"
    )
    price_economy = models.IntegerField()
    price_business = models.IntegerField()
    # if economy rows are from 11 it means that 1-10 rows are business class
    # (and the rest are economy to end of airplane's rows)
    rows_economy_from = models.IntegerField()
    luggage_price_1_kg = models.DecimalField(decimal_places=2, max_digits=8)

    class Meta:
        ordering = ["departure_time"]

    def __str__(self):
        return f"{self.route.source.name} -> {self.route.destination.name}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.created_at.strftime("%Y-%m-%d %H:%M"))


class SnacksAndDrinks(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(null=True, blank=True, upload_to=create_custom_path)

    def __str__(self):
        return f"{self.name}, PRICE={self.price}$"


class MealOption(models.Model):
    MEAL_TYPE_CHOICES = [
        ("1", "Standard"),
        ("2", "Vegetarian"),
        ("3", "Children's Portion"),
        ("4", "No Meal")
    ]
    name = models.CharField(max_length=255, unique=True)
    meal_type = models.CharField(
        max_length=30,
        choices=MEAL_TYPE_CHOICES,
        default="4"
    )
    weight = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(null=True, blank=True, upload_to=create_custom_path)

    def __str__(self):
        return f"Name: {self.name}, type: {self.get_meal_type_display()}, weight: {self.weight}, PRICE={self.price}$"


class ExtraEntertainmentAndComfort(models.Model):
    name = models.CharField(
        max_length= 55,
    )
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(null=True, blank=True, upload_to=create_custom_path)

    def __str__(self):
        return f"{self.name} -> {self.price}$"


# for example "new year discount 5%" etc.
class DiscountCoupon(models.Model):
    name = models.CharField(max_length=255)
    valid_until = models.DateTimeField(validators=[validate_discount_date])
    code = models.CharField(validators=[validate_discount_coupon_code])
    discount = models.IntegerField(null=False)
    is_active = models.BooleanField(blank=True, default=True)

    def __str__(self):
        return f"Coupon Name: {self.name}, Code: {self.code}"


class Ticket(models.Model):
    identifier = models.CharField(default=create_custom_uuid_ticket(), null=True, blank=True)
    row = models.IntegerField()
    letter = models.CharField(max_length=1)
    is_child = models.BooleanField(default=False, null=True, blank=True)
    discount = models.IntegerField(
        default=0,
        blank=True,
        null=True,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ]
    )
    has_luggage = models.BooleanField(blank=True, default=False)
    luggage_weight = models.DecimalField(decimal_places=2, max_digits=8, null=True, blank=True)
    flight = models.ForeignKey(
        Flight,
        on_delete=models.SET_NULL,
        related_name="tickets",
        null=True
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="tickets",
        null=True,
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    meal_option = models.ForeignKey(
        MealOption,
        on_delete=models.SET_NULL,
        related_name="tickets",
        null=True,
        blank=True
    )
    extra_entertainment_and_comfort = models.ManyToManyField(
        ExtraEntertainmentAndComfort,
        related_name="tickets",
        blank=True,
    )
    snacks_and_drinks = models.ManyToManyField(
        SnacksAndDrinks,
        related_name="tickets",
        blank=True,
    )
    is_business = models.BooleanField(null=True, blank=True, default=False)
    discount_coupon = models.ForeignKey(
        DiscountCoupon,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    @staticmethod
    def validate_ticket(row, letter, airplane, error_to_raise):
        if not (1 <= row <= airplane.rows):
            raise error_to_raise(
                {f"The row must be in range: 1 - {airplane.rows}"}
            )
        if letter not in airplane.list_of_seats:
            raise error_to_raise(
                {f"The seat must be in range {airplane.list_of_seats}"}
            )

    @staticmethod
    def validate_discount_coupon(code, error_to_raise):
        if not DiscountCoupon.objects.filter(code=code).exists():
            raise error_to_raise(
                {f"Invalid discount code: '{code}'"}
            )

    def clean(self):
        Ticket.validate_ticket(
            row=self.row,
            letter=self.letter,
            airplane=self.flight.airplane,
            error_to_raise=ValidationError
        )
        if self.discount_coupon:
            Ticket.validate_discount_coupon(
            code=self.discount_coupon.code,
            error_to_raise=ValidationError
        )

    def save(
        self,
        force_insert = False,
        force_update = False,
        using = None,
        update_fields = None,
    ):
        self.full_clean()
        return super(Ticket, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f"{self.flight}, row: {self.row}, seat: {self.letter}"

    class Meta:
        ordering = ["row", "letter"]
        unique_together = ("flight", "letter", "row")
