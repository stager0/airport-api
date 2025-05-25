from rest_framework.exceptions import ValidationError


def validate_discount_coupon_code(value: str) -> ValidationError | None:
    if len(value) < 10 or len(value) > 10:
        raise ValidationError(f"The code: '{value}' must be 10 symbols long")
    if not value.isalnum():
        raise ValidationError(f"The code: '{value}' must contain only letters or numbers")
