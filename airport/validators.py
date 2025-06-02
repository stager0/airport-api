from datetime import datetime

from django.utils import timezone
from django.utils.timezone import make_aware
from rest_framework.exceptions import ValidationError


def validate_discount_coupon_code(value: str) -> ValidationError | None:
    if len(value) < 10 or len(value) > 10:
        raise ValidationError(f"The code: '{value}' must be 10 symbols long")
    if not value.isalnum():
        raise ValidationError(f"The code: '{value}' must contain only letters or numbers")

def validate_discount_date(date: datetime) -> ValidationError | None:
    if date < timezone.now() :
        raise ValidationError(f"The date (valid until) must be later than {timezone.now}")
    if date > make_aware(datetime(2099, 12, 12)):
        raise ValidationError(f"The date must be earlier then {date}")
