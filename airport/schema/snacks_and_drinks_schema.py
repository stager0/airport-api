from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
    OpenApiParameter,
    extend_schema_view
)

from airport.serializers import SnacksAndDrinksSerializer


snacks_and_drinks_schema = extend_schema_view(
    list=extend_schema(
        summary="Get a list of all Snacks and Drinks",
        description="Returns a list of all Snacks and Drinks available in the system",
        tags=["snacks_and_drinks"],
        request=SnacksAndDrinksSerializer,
        parameters=[
            OpenApiParameter(
                name="name", description="Filter by Name (water, cola, fanta etc.)",
                required=False, type=str
            )
        ],
        responses={
            200: SnacksAndDrinksSerializer(many=True),
            401: OpenApiResponse(description="Authentication credentials were not provided"),
        },
        examples=[
            OpenApiExample(
                name="Snacks And Drinks List Example",
                value=[
                    {
                        "id": 1,
                        "name": "Coca-Cola 0.5",
                        "price": 2.00
                    },
                    {
                        "id": 2,
                        "name": "Fanta 0.5",
                        "price": 2.00
                    },
                ],
                response_only=True
            )
        ]
    ),
    create=extend_schema(
        summary="Create a new Snack Or Drink",
        description="Creates a new Snack or Drink with provided data (name, price)",
        tags=["snacks_and_drinks"],
        request=SnacksAndDrinksSerializer,
        responses={
            201: SnacksAndDrinksSerializer,
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            400: OpenApiResponse(
                description="Bad request",
                examples=[
                    OpenApiExample(
                        "Empty (incorrect) name and price",
                        value={
                            "name": ["This field may not be blank."],
                            "price": ["A valid number is required."],
                        },
                        status_codes=["400"]
                    )
                ]
            )
        },
        examples=[
            OpenApiExample(
                "Create example",
                value={"name": "Tee", "price": 1.99},
                request_only=True
            )
        ]
    )
)