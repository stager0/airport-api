from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
    OpenApiParameter,
    extend_schema_view
)

from airport.serializers import CrewSerializer, CrewImageSerializer

crew_schema = extend_schema_view(
    list=extend_schema(
        summary="Get a list of all Crews(workers)",
        description="Retrieve a list of all actual Crews in format (first_name, last_name, position)",
        tags=["crew"],
        request=CrewSerializer,
        responses={
            200: CrewSerializer(many=True),
            401: OpenApiResponse(description="Authentication credentials were not provided")
        },
        parameters=[
            OpenApiParameter(
                name="first_name", description="Filter by first_name",
                required=False, type=str
            ),
            OpenApiParameter(
                name="last_name", description="Filter by last_name",
                required=False, type=str
            ),
            OpenApiParameter(
                name="position", description="Filter by position",
                required=False, type=str
            )
        ],
        examples=[
            OpenApiExample(
                "Item from Crew List Example",
                value={
                    "id": 1,
                    "first_name": "James",
                    "last_name": "Kirk",
                    "position": "CAPTAIN"
                },
            )
        ]
    ),
    create=extend_schema(
        summary="Create a Crew Person",
        description="Creates a crew Person with provided data (first_name, last_name, position)",
        tags=["crew"],
        request=CrewSerializer,
        responses={
            201: CrewSerializer,
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            400: OpenApiResponse(
                description="Bad Request",
                examples=[
                    OpenApiExample(
                        "Empty first_name and last_name",
                        value={
                            "first_name": ["This field may not be blank."],
                            "last_name": ["This field may not be blank."]
                        },
                        status_codes=["400"]
                    )
                ]
            )
        },
        examples=[
            OpenApiExample(
                "Create new Crew Person",
                value={
                    "first_name": "John",
                    "last_name": "Muller",
                    "position": "CAPTAIN"
                },
                request_only=True
            )
        ]
    ),
    upload_image=extend_schema(
        summary="Upload an Image",
        description="Uploads an Airplane Image",
        tags=["crew"],
        request=CrewImageSerializer,
        responses={
            200: CrewImageSerializer,
            403: OpenApiResponse(description="You do not have permission to perform this action."),
        },
    )
)