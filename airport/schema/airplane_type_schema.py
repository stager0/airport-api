from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
    extend_schema_view
)

from airport.models import AirplaneType
from airport.serializers import AirplaneTypeSerializer


airport_type_schema = extend_schema_view(
    list=extend_schema(
        summary="Get a list of all Airplane Types",
        description="Retrieve a list of all Airplane Types (owned by the company)",
        tags=["airplane_type"],
        request=AirplaneTypeSerializer,
        responses={
            200: AirplaneTypeSerializer(many=True),
            401: OpenApiResponse(description="Authentication credentials were not provided")
        },
        examples=[
            OpenApiExample(
                "Item from AirplaneType List Example",
                value={
                    "id": 1,
                    "name": "Boeing 777"
                },
                response_only=True
            )
        ]
    ),
    create=extend_schema(
        summary="Create an Airplane Type",
        description="Creates an Airplane Type with provided name",
        tags=["airplane_type"],
        request=AirplaneType,
        responses={
            201: AirplaneType,
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            400: OpenApiResponse(
                description="Bad Request",
                examples=[
                    OpenApiExample(
                        "Empty Airplane Name",
                        value={
                            "name": ["This field may not be blank."]
                        },
                        status_codes=["400"]
                    )
                ]
            )
        },
        examples=[
            OpenApiExample(
                "Create new Airplane Type",
                value={
                    "name": "Boeing",
                },
                request_only=True
            )
        ]
    ),
)