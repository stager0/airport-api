from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
    OpenApiParameter,
    OpenApiExample
)

from airport.serializers import (
    RouteListSerializer,
    RouteSerializer
)


route_schema = extend_schema_view(
    list=extend_schema(
        summary="Get a list of all Routes",
        description="Retrieve all possible Routes in format(distance, source, destination)",
        request=RouteListSerializer,
        tags=["route"],
        responses={
            200: RouteListSerializer(many=True),
            401: OpenApiResponse(description="Authentication credentials were not provided")
        },
        parameters=[
            OpenApiParameter(
                name="source", description="Filter by source (example: Kiev, Berlin, Paris)",
                required=False, type=str
            ),
            OpenApiParameter(
                name="destination", description="Filter by destination (example: Kiev, Berlin, Paris)",
                required=False, type=str
            ),
            OpenApiParameter(
                name="source_airport",
                description="Filter by source airport name (example: Boryspil International Airport)",
                required=False, type=str
            ),
            OpenApiParameter(
                name="destination_airport",
                description="Filter by destination airport name (example: Boryspil International Airport)",
                required=False, type=str
            )
        ],
        examples=[
            OpenApiExample(
                "Route from list example",
                value=[
                    {
                        "id": 10,
                        "distance": 690,
                        "source": {
                            "id": 8,
                            "name": "Boryspil International Airport",
                            "closest_big_city": "Kyiv"
                        },
                        "destination": {
                            "id": 9,
                            "name": "Warsaw Chopin Airport",
                            "closest_big_city": "Warsaw"
                        }
                    },
                ],
                request_only=True
            )
        ]
    ),
    create=extend_schema(
        summary="Create a new Route",
        description="Create a new with provided data (distance, source, destination)",
        request=RouteSerializer,
        tags=["route"],
        responses={
            201: RouteSerializer,
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            400: OpenApiResponse(
                description="Bad Request",
                examples=[
                    OpenApiExample(
                        "Empty distance, source and destination",
                        value={
                            "distance": ["This field is required."],
                            "source": ["This field is required."],
                            "destination": ["This field is required."]
                        },
                        status_codes=["400"]
                    )
                ]
            )
        },
        examples=[
            OpenApiExample(
                "Create a new Route Example ",
                value=[
                    {
                        "distance": 1234,
                        "source": 1,
                        "destination": 2
                    }
                ],
                request_only=True
            )
        ]
    )
)