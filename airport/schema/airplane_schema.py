from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
    extend_schema_view
)

from airport.serializers import AirplaneSerializer, AirplaneImageSerializer

airplane_schema = extend_schema_view(
    list=extend_schema(
        summary="Get a list of all Airplanes",
        description="Retrieve a list of all Airplanes in format (name, rows, letters_in_row, airplane_type)",
        tags=["airplane"],
        request=AirplaneSerializer,
        responses={
            200: AirplaneSerializer(many=True),
            401: OpenApiResponse(description="Authentication credentials were not provided")
        },
        examples=[
            OpenApiExample(
                "Item from Airplane List Example",
                value={
                    "id": 1,
                    "name": "Sky Explorer",
                    "rows": 30,
                    "letters_in_row": "ABCDEF",
                    "airplane_type": 1
                },
                response_only=True
            )
        ]
    ),
    create=extend_schema(
        summary="Create an Airplane",
        description="Creates an Airplane with provided data (name, rows, letters_in_row, airplane_type(pk))",
        tags=["airplane"],
        request=AirplaneSerializer,
        responses={
            201: AirplaneSerializer,
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            400: OpenApiResponse(
                description="Bad Request",
                examples=[
                    OpenApiExample(
                        "Empty name, rows, letters_on_row, airplane_type",
                        value={
                            "name": ["This field may not be blank."],
                            "rows": ["A valid integer is required."],
                            "letters_in_row": ["This field may not be blank."],
                            "airplane_type": ["This field may not be null."]
                        },
                        status_codes=["400"]
                    )
                ]
            )
        },
        examples=[
            OpenApiExample(
                "Create a new Airplane",
                value={
                    "name": "Sky Explorer Turbo",
                    "rows": 25,
                    "letters_in_row": "ABCDE",
                    "airplane_type": 1
                },
                request_only=True
            )
        ]
    ),
    upload_image=extend_schema(
        summary="Upload an Image",
        description="Uploads an Airplane Image",
        tags=["airplane"],
        request=AirplaneImageSerializer,
        responses={
            200: AirplaneImageSerializer,
            403: OpenApiResponse(description="You do not have permission to perform this action."),
        },
    )
)