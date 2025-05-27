from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema, OpenApiParameter, extend_schema_view

from airport.serializers import AirportSerializer


airport_schema = extend_schema_view(
    list=extend_schema(
        summary="Get a list of Airports",
        description="Retrieve a list of all available Airports (from which this company flies)",
        tags=["airport"],
        request=AirportSerializer,
        responses={
            200: AirportSerializer(many=True),
            401: OpenApiResponse(description="Authentication credentials were not provided")
        },
        parameters=[
            OpenApiParameter(
                name="closest_big_city", description="Filter by closest_big_city",
                required=False, type=str
            ),
            OpenApiParameter(
                name="airport_name", description="Filter by airport_name",
                required=False, type=str
            )
        ],
        examples=[
            OpenApiExample(
                "List Example",
                value={
                    "id": 1,
                    "name": "JFK International Airport",
                    "closest_big_city": "New York City"
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create an Airport",
        description="Create an Airport with provided data (name (airport name), closest big city)",
        tags=["airport"],
        request=AirportSerializer,
        responses={
            201: AirportSerializer,
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            400: OpenApiResponse(
                description="Bad Request",
                examples=[
                    OpenApiExample(
                        "Empty name and closest_big_city",
                        value={
                            "name": ["This field may not be blank."],
                            "closest_big_city": ["This field may not be blank."]
                        },
                        status_codes=["400"]
                    )
                ]
            )
        },
        examples=[
            OpenApiExample(
                "Create new Airport",
                value={
                    "name": "Airport Boryspil, Kiev",
                    "closest_big_city": "Kiev"
                },
                request_only=True
            )
        ]
    )
)