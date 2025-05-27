from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema, OpenApiParameter, extend_schema_view

from airport.serializers import MealOptionSerializer


meal_option_schema = extend_schema_view(
    list=extend_schema(
        summary="Retrieve a list of all Meal Options",
        description="Returns a list of all Meal Options available in the system",
        tags=["MealOption"],
        parameters=[
            OpenApiParameter(
                name="name", description="Filter by MealOption Name (Chicken Curry etc.)",
                required=False, type=str
            ),
            OpenApiParameter(
                name="meal_type", description="Filter by Meal Option Type Id",
                required=False, type=int
            ),
            OpenApiParameter(
                name="price",
                description="Filter to this price (if ?price=20 -> return all Meal Option which cost less than 20 )",
                required=False, type=int
            )
        ],
        responses={
            200: MealOptionSerializer(many=True),
            401: OpenApiResponse(description="Authentication credentials were not provided")
        },
        examples=[
            OpenApiExample(
                name="Meal Option List Example",
                value=[
                    {"id": 2, "name": "Beef Steak", "meal_type": "1", "weight": 400, "price": 15.00}
                ],
                response_only=True
            )
        ]
    ),
    create=extend_schema(
        summary="Create a new Meal Option",
        description="Creates a new Meal Option with provided data (name, meal_type, weight, price)",
        tags=["MealOption"],
        request=MealOptionSerializer,
        responses={
            201: MealOptionSerializer,
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            400: OpenApiResponse(
                description="Bad request",
                examples=[
                    OpenApiExample(
                        "Incorrect price and empty name",
                        value={
                            "name": ["This field may not be blank."],
                            "price": ["A valid number is required."]
                        },
                        status_codes=["400"]
                    )
                ]
            ),
        },
        examples=[
            OpenApiExample(
                name="Create Meal Type Example",
                value=[
                    {"name": "Beef Steak BBQ", "meal_type": "1", "weight": 500, "price": 19.00},
                ],
                request_only=True
            )
        ]
    ),
)