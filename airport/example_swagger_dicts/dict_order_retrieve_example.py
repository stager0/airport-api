example_order_retrieve_dict = {
    "id": 33,
    "created_at": "2025-05-26T12:01:25.173735Z",
    "total_price": "685.48",
    "user": {
        "id": 1,
        "username": "admin"
    },
    "tickets": [
        {
            "id": 66,
            "row": 9,
            "letter": "C",
            "discount": 0,
            "has_luggage": "true",
            "flight": {
                "id": 1,
                "departure_time": "2025-07-10T08:00:00Z",
                "arrival_time": "2025-07-10T15:30:00Z",
                "route": {
                    "id": 1,
                    "distance": 5567,
                    "source": {
                        "id": 1,
                        "name": "JFK International Airport",
                        "closest_big_city": "New York City"
                    },
                    "destination": {
                        "id": 2,
                        "name": "Heathrow Airport",
                        "closest_big_city": "London"
                    }
                },
                "airplane": {
                    "id": 1,
                    "name": "Sky Explorer",
                    "rows": 30,
                    "letters_in_row": "ABCDEF",
                    "airplane_type": {
                        "id": 1,
                        "name": "Boeing 737"
                    }
                },
                "luggage_price_1_kg": "5.50"
            },
            "meal_option": {
                "id": 6,
                "name": "Fish and Potatoes",
                "meal_type": "1",
                "weight": 360,
                "price": "13.50"
            },
            "extra_entertainment_and_comfort": [
                {
                    "id": 1,
                    "name": "Tablet with movies/games",
                    "price": "9.99"
                },
                {
                    "id": 2,
                    "name": "Wireless headphones",
                    "price": "7.49"
                },
                {
                    "id": 3,
                    "name": "Pillow and blanket",
                    "price": "5.00"
                },
                {
                    "id": 4,
                    "name": "Sleep mask and earplugs",
                    "price": "3.50"
                },
                {
                    "id": 5,
                    "name": "In-flight WI-FI access",
                    "price": "12.00"
                }
            ],
            "snacks_and_drinks": [
                {
                    "id": 1,
                    "name": "Coca-Cola 0.5",
                    "price": "2.00"
                },
                {
                    "id": 2,
                    "name": "Fanta 0.5",
                    "price": "2.00"
                },
                {
                    "id": 3,
                    "name": "Juice 0.5",
                    "price": "2.50"
                },
                {
                    "id": 4,
                    "name": "Cup of coffee 0.33",
                    "price": "3.00"
                },
                {
                    "id": 5,
                    "name": "Red-Bull 0.25",
                    "price": "3.50"
                },
                {
                    "id": 6,
                    "name": "Water(PET), 0.5",
                    "price": "1.50"
                }
            ],
            "discount_coupon": "null",
            "luggage_weight": "49.00",
            "ticket_price": 350,
            "luggage_price": 269.5,
            "extra_price": 65.98
        }
    ]
}
