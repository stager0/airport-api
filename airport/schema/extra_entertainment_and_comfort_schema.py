from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
    OpenApiParameter,
    extend_schema_view
)

from airport.serializers import ExtraEntertainmentAndComfortSerializer


extra_entertainment_and_comfort_schema = extend_schema_view(
    list=extend_schema(
        summary="Get all from Extra Entertainment and Comfort",
        description="Retrieve a list with all Extra Entertainment and Comfort items",
        tags=["extra_entertainment_and_comfort"],
        request=ExtraEntertainmentAndComfortSerializer,
        parameters=[
            OpenApiParameter(
                name="name", description="Filter by item name (tablet, pillow etc.)",
                required=False, type=str
            )
        ],
        responses={
            200: ExtraEntertainmentAndComfortSerializer(many=True),
            401: OpenApiResponse(description="Authentication credentials were not provided")
        },
        examples=[
            OpenApiExample(
                "List Example",
                value=[
                    {"id": 1, "name": "Tablet with movies/games", "price": "9.99"},
                ],
                response_only=True
            )
        ]
    ),
    create=extend_schema(
        summary="Create a new Extra Entertainment and Comfort item",
        description="Create a new item Extra Entertainment and Comfort by provided data (name, price)",
        request=ExtraEntertainmentAndComfortSerializer,
        tags=["extra_entertainment_and_comfort"],
        responses={
            201: ExtraEntertainmentAndComfortSerializer,
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            400: OpenApiResponse(
                description="Bad request",
                examples=[
                    OpenApiExample(
                        "Empty (incorrect) Name and Price",
                        value={
                            "name": ["This field may not be blank."],
                            "price": ["A valid number is required."]
                        },
                        status_codes=["400"]
                    ),
                ]
            )
        },
        examples=[
            OpenApiExample(
                "Create Example",
                value={
                    "name": "Tablet",
                    "price": 17.50
                },
                request_only=True
            )
        ]
    )
)