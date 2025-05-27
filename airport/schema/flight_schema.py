from drf_spectacular.utils import OpenApiResponse, extend_schema, OpenApiExample, OpenApiParameter, extend_schema_view

from airport.example_swagger_dicts.dicts_flight_examples import dict_create_example, dict_retrieve_example, \
    errors_when_there_are_not_fields_provided, dict_flight_list_example, dict_flight_update_empty_example
from airport.serializers import FlightSerializer, FlightRetrieveSerializer, FlightListSerializer

flight_schema = extend_schema_view(
    list=extend_schema(
        summary="Get a list of all Flights",
        description="Retrieve a list of all Flights",
        request=FlightListSerializer(many=True),
        tags=["flight"],
        responses={
            200: FlightListSerializer(many=True),
            401: OpenApiResponse(description="Authentication credentials were not provided"),
        },
        parameters=[
            OpenApiParameter(
                name="destination", description="Filter by destination (Kiev, Berlin, Paris)",
                required=False, type=str
            ),
            OpenApiParameter(
                name="source", description="Filter by source (Kiev, Berlin, Paris)",
                required=False, type=str
            ),
            OpenApiParameter(
                name="airplane", description="Filter by airplane name (example: Sky Explorer)",
                required=False, type=str
            ),
            OpenApiParameter(
                name="date_from", description="Filter by date (from given date)",
                required=False, type=str
            ),
            OpenApiParameter(
                name="date_to", description="Filter by date (to given date)",
                required=False, type=str
            )
        ],
        examples=[
            OpenApiExample(
                "Flight from the list",
                value=[
                    dict_flight_list_example
                ],
                response_only=True
            )
        ]
    ),
    create=extend_schema(
        summary="Create a new Flight",
        description="Create a new flight with provided data ("
                    "departure_time, arrival_time, route, airplane",
        tags=["flight"],
        request=FlightSerializer,
        responses={
            201: FlightSerializer,
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            400: OpenApiResponse(
                description="Bad Request",
                examples=[
                    OpenApiExample(
                        "Empty fields (no data given)",
                        value=[
                            errors_when_there_are_not_fields_provided
                        ],
                        status_codes=["400"]
                    )
                ]
            )
        },
        examples=[
            OpenApiExample(
                "Create Flight Example",
                value=[
                    dict_create_example
                ],
                request_only=True
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve a Flight by given ID",
        description="Get one Flight Object by given ID, it returns all information about Flight. "
                    "(information about count of seats and rows (letters) are from Airplane Model)",
        request=FlightRetrieveSerializer,
        tags=["flight"],
        responses={
            200: FlightRetrieveSerializer,
            404: OpenApiResponse(description="No Flight matches the given query.")
        },
        examples=[
            OpenApiExample(
                "Retrieve Example",
                value=[
                    dict_retrieve_example
                ]
            )
        ]
    ),
    update=extend_schema(
        summary="Update a Flight completely",
        description="Fully update all Flight fields by provided data",
        tags=["flight"],
        request=FlightSerializer,
        responses={
            200: FlightSerializer,
            404: OpenApiResponse(description="No Flight matches the given query."),
            400: OpenApiResponse(
                description="Bad Request",
                examples=[
                    OpenApiExample(
                        "Empty update (no given data)",
                        value=[
                            dict_flight_update_empty_example
                        ],
                        status_codes=["400"]
                    )
                ]
            )
        },
        examples=[
            OpenApiExample(
                "Update Example",
                value=[
                    dict_create_example
                ],
                request_only=True
            )
        ]
    ),
    partial_update=extend_schema(
        summary="Partially update a Flight",
        description="Update one or more fields of given Flight (ID)",
        request=FlightSerializer,
        tags=["flight"],
        responses={
            200: FlightSerializer,
            404: OpenApiResponse(description="No Flight matches the given query."),
            400: OpenApiResponse(
                description="Bad Request",
                examples=[
                    OpenApiExample(
                        "Empty field",
                        value="JSON parse error - Expecting value: line 5 column 14 (char 119)",
                        status_codes=["400"]
                    ),
                ],
            )
        },
        examples=[
            OpenApiExample(
                "Partial Update Flight",
                value=[
                    {
                        "price_economy": 199,
                        "price_business": 299,
                    }
                ],
                request_only=True
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete a Flight",
        description="Remove a flight by provided ID from the system",
        tags=["flight"],
        responses={
            204: OpenApiResponse(description="Item successfully deleted"),
            404: OpenApiResponse(description="No Flight matches the given query."),
            403: OpenApiResponse(description="You do not have permission to perform this action.")
        }
    )
)