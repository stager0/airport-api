from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema, extend_schema_view

from airport.example_swagger_dicts.dict_order_retrieve_example import example_order_retrieve_dict
from airport.serializers import OrderRetrieveSerializer, OrderSerializer, OrderListSerializer

order_schema = extend_schema_view(
    list=extend_schema(
        summary="Get all Orders (only for actual user)",
        description="Retrieve list of all Orders for actual(request) user. User can see only personal orders",
        tags=["order"],
        responses={
            200: OrderListSerializer,
            401: OpenApiResponse(description="Authorisation credentials were not provided"),
        },
        request=OrderListSerializer,
        examples=[
            OpenApiExample(
                "Item from Orders List, Example",
                value={
                    "id": 33,
                    "created_at": "2025-05-26T12:01:25.173735Z",
                    "total_price": "685.48",
                    "user": {
                        "id": 1,
                        "username": "admin"
                    },
                    "count_of_tickets": 1,
                    "source": "New York City",
                    "destination": "London"
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create an Order",
        description="Creates an Order and tickets, it counts order.total_price and etc. It's need only to add all tickets",
        request=OrderSerializer,
        tags=["order"],
        responses={
            201: OrderSerializer,
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            400: OpenApiResponse(
                description="Bad Request",
                examples=[
                    OpenApiExample(
                        "No Ticket",
                        value={
                            "tickets": {
                                "non_field_errors": [
                                    "This list may not be empty."
                                ]
                            }
                        },
                        status_codes=["400"]
                    )
                ]
            )
        },
        examples=[
            OpenApiExample(
                "Create new Order Example",
                value=[
                    {
                        "tickets": [
                            {
                                "row": 12,
                                "letter": "C",
                                "has_luggage": "true",
                                "flight": 1,
                                "meal_option": 6,
                                "extra_entertainment_and_comfort": "[1, 2, 3, 4, 5]",
                                "snacks_and_drinks": "[6, 1, 2, 3, 4, 5]",
                                "luggage_weight": 49.0
                            }
                        ],
                    }
                ],
                request_only=True
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Get Single Item by Id",
        description="Retrieve detail information about an order (all info about tickets, prices and etc.) using its unique ID",
        tags=["order"],
        request=OrderRetrieveSerializer,
        responses={
            200: OrderRetrieveSerializer,
            404: OpenApiResponse(description="No Order matches the given query.")
        },
        examples=[
            OpenApiExample(
                "Retrieve Example",
                value=[
                    example_order_retrieve_dict
                ]
            )
        ]
    )
)