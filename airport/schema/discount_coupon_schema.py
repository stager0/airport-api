from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema

from airport.serializers import DiscountCouponSerializer

discount_coupon_schema = extend_schema_view(
    list=extend_schema(
        summary="Get a list of all Discount Coupons",
        description="Retrieve a list of all Discount Coupons in format (name, valid_until, code, discount)",
        tags=["discount_coupon"],
        request=DiscountCouponSerializer,
        responses={
            200: DiscountCouponSerializer(many=True),
            401: OpenApiResponse(description="Authentication credentials were not provided")
        },
        examples=[
            OpenApiExample(
                "Item from Airplane List Example",
                value={
                    "id": 4,
                    "name": "Expired Deal",
                    "valid_until": "2024-12-31T23:59:59Z",
                    "code": "OLD111DEAL",
                    "discount": 20
                },
            )
        ]
    ),
    create=extend_schema(
        summary="Create an Discount Coupon",
        description="Create an Discount Coupon with provided data (name, valid_until, code, discount (0-100))",
        tags=["discount_coupon"],
        request=DiscountCouponSerializer,
        responses={
            201: DiscountCouponSerializer,
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            400: OpenApiResponse(
                description="Bad Request",
                examples=[
                    OpenApiExample(
                        "Empty name, valid_until, code, discount",
                        value={
                            "name": ["This field may not be blank."],
                            "valid_until": ["Datetime has wrong format. Use one of these formats instead: "
                                            "YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]."],
                            "code": ["This field may not be blank."],
                            "discount": ["A valid integer is required."]
                        },
                        status_codes=["400"]
                    )
                ]
            )
        },
        examples=[
            OpenApiExample(
                "Create a new Discount Coupon",
                value={
                    "name": "New year BOOM",
                    "valid_until": "2024-12-31T23:59:59Z",
                    "code": "NEWYEAR111",
                    "discount": 25
                },
                request_only=True
            )
        ]
    )
)