dict_flight_list_example = {
    "id": 1,
    "departure_time": "2025-07-10T08:00:00Z",
    "arrival_time": "2025-07-10T15:30:00Z",
    "route": {
        "distance": 5567,
        "source": {
            "closest_big_city": "New York City"
        },
        "destination": {
            "closest_big_city": "London"
        }
    },
    "airplane": {
        "name": "Sky Explorer"
    },
    "places_available": 158,
    "business_places_available": 64,
    "economy_places_available": 94
},

errors_when_there_are_not_fields_provided = {
    "departure_time": [
        "This field is required."
    ],
    "arrival_time": [
        "This field is required."
    ],
    "route": [
        "This field is required."
    ],
    "airplane": [
        "This field is required."
    ],
    "crew": [
        "This field is required."
    ],
    "price_economy": [
        "This field is required."
    ],
    "price_business": [
        "This field is required."
    ],
    "rows_economy_from": [
        "This field is required."
    ],
    "luggage_price_1_kg": [
        "This field is required."
    ]
}

dict_create_example = {
    "departure_time": "2025-05-30T23:13:00Z",
    "arrival_time": "2025-05-30T15:08:00Z",
    "route": 62,
    "airplane": 3,
    "crew": [
        1,
        2,
        3,
        4,
        5
    ],
    "price_economy": 120,
    "price_business": 190,
    "rows_economy_from": 12,
    "luggage_price_1_kg": "1.98"
}

dict_retrieve_example = {
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
    "crew": [
        {
            "id": 1,
            "first_name": "James",
            "last_name": "Kirk",
            "position": "CAPTAIN"
        },
        {
            "id": 2,
            "first_name": "William",
            "last_name": "Riker",
            "position": "FIRST_OFFICER"
        },
        {
            "id": 3,
            "first_name": "Uhura",
            "last_name": "Nyota",
            "position": "LEAD_FLIGHT_ATTENDANT"
        },
        {
            "id": 4,
            "first_name": "Beverly",
            "last_name": "Crusher",
            "position": "FLIGHT_ATTENDANT"
        },
        {
            "id": 5,
            "first_name": "Deanna",
            "last_name": "Troi",
            "position": "FLIGHT_ATTENDANT"
        }
    ],
    "price_economy": 350,
    "price_business": 700,
    "rows_economy_from": 11,
    "luggage_price_1_kg": "5.50",
    "all_free_places": [
        "Economy: [{'row': 12, 'letter': 'B'}, {'row': 12, 'letter': 'D'}, {'row': 12, 'letter': 'E'}, {'row': 13, 'letter': 'A'}, {'row': 13, 'letter': 'B'}, {'row': 13, 'letter': 'D'}, {'row': 13, 'letter': 'E'}, {'row': 13, 'letter': 'F'}, {'row': 14, 'letter': 'A'}, {'row': 14, 'letter': 'B'}, {'row': 14, 'letter': 'C'}, {'row': 14, 'letter': 'D'}, {'row': 14, 'letter': 'E'}, {'row': 14, 'letter': 'F'}, {'row': 15, 'letter': 'B'}, {'row': 15, 'letter': 'D'}, {'row': 15, 'letter': 'E'}, {'row': 15, 'letter': 'F'}, {'row': 16, 'letter': 'A'}, {'row': 16, 'letter': 'B'}, {'row': 16, 'letter': 'C'}, {'row': 16, 'letter': 'D'}, {'row': 16, 'letter': 'E'}, {'row': 16, 'letter': 'F'}, {'row': 17, 'letter': 'B'}, {'row': 17, 'letter': 'C'}, {'row': 17, 'letter': 'D'}, {'row': 17, 'letter': 'E'}, {'row': 17, 'letter': 'F'}, {'row': 18, 'letter': 'A'}, {'row': 18, 'letter': 'B'}, {'row': 18, 'letter': 'C'}, {'row': 18, 'letter': 'E'}, {'row': 18, 'letter': 'F'}, {'row': 19, 'letter': 'A'}, {'row': 19, 'letter': 'B'}, {'row': 19, 'letter': 'C'}, {'row': 19, 'letter': 'D'}, {'row': 19, 'letter': 'E'}, {'row': 19, 'letter': 'F'}, {'row': 20, 'letter': 'A'}, {'row': 20, 'letter': 'B'}, {'row': 20, 'letter': 'C'}, {'row': 20, 'letter': 'D'}, {'row': 20, 'letter': 'E'}, {'row': 20, 'letter': 'F'}, {'row': 21, 'letter': 'A'}, {'row': 21, 'letter': 'B'}, {'row': 21, 'letter': 'C'}, {'row': 21, 'letter': 'D'}, {'row': 21, 'letter': 'E'}, {'row': 21, 'letter': 'F'}, {'row': 22, 'letter': 'A'}, {'row': 22, 'letter': 'B'}, {'row': 22, 'letter': 'C'}, {'row': 22, 'letter': 'D'}, {'row': 22, 'letter': 'E'}, {'row': 22, 'letter': 'F'}, {'row': 23, 'letter': 'A'}, {'row': 23, 'letter': 'B'}, {'row': 23, 'letter': 'C'}, {'row': 23, 'letter': 'D'}, {'row': 23, 'letter': 'E'}, {'row': 23, 'letter': 'F'}, {'row': 24, 'letter': 'A'}, {'row': 24, 'letter': 'B'}, {'row': 24, 'letter': 'C'}, {'row': 24, 'letter': 'D'}, {'row': 24, 'letter': 'E'}, {'row': 24, 'letter': 'F'}, {'row': 25, 'letter': 'A'}, {'row': 25, 'letter': 'B'}, {'row': 25, 'letter': 'C'}, {'row': 25, 'letter': 'D'}, {'row': 25, 'letter': 'E'}, {'row': 26, 'letter': 'A'}, {'row': 26, 'letter': 'B'}, {'row': 26, 'letter': 'C'}, {'row': 26, 'letter': 'D'}, {'row': 26, 'letter': 'E'}, {'row': 26, 'letter': 'F'}, {'row': 27, 'letter': 'A'}, {'row': 27, 'letter': 'B'}, {'row': 27, 'letter': 'C'}, {'row': 27, 'letter': 'D'}, {'row': 27, 'letter': 'E'}, {'row': 27, 'letter': 'F'}, {'row': 28, 'letter': 'A'}, {'row': 28, 'letter': 'B'}, {'row': 28, 'letter': 'C'}, {'row': 28, 'letter': 'D'}, {'row': 28, 'letter': 'E'}, {'row': 28, 'letter': 'F'}, {'row': 29, 'letter': 'A'}, {'row': 29, 'letter': 'B'}, {'row': 29, 'letter': 'C'}, {'row': 29, 'letter': 'D'}, {'row': 29, 'letter': 'E'}, {'row': 29, 'letter': 'F'}, {'row': 30, 'letter': 'A'}, {'row': 30, 'letter': 'B'}, {'row': 30, 'letter': 'C'}, {'row': 30, 'letter': 'D'}, {'row': 30, 'letter': 'E'}, {'row': 30, 'letter': 'F'}]",
        "Business: [{'row': 1, 'letter': 'A'}, {'row': 1, 'letter': 'B'}, {'row': 1, 'letter': 'C'}, {'row': 1, 'letter': 'D'}, {'row': 1, 'letter': 'E'}, {'row': 2, 'letter': 'A'}, {'row': 2, 'letter': 'B'}, {'row': 2, 'letter': 'C'}, {'row': 2, 'letter': 'E'}, {'row': 3, 'letter': 'A'}, {'row': 3, 'letter': 'B'}, {'row': 3, 'letter': 'C'}, {'row': 3, 'letter': 'D'}, {'row': 3, 'letter': 'E'}, {'row': 4, 'letter': 'A'}, {'row': 4, 'letter': 'B'}, {'row': 4, 'letter': 'C'}, {'row': 4, 'letter': 'D'}, {'row': 4, 'letter': 'E'}, {'row': 5, 'letter': 'A'}, {'row': 5, 'letter': 'C'}, {'row': 5, 'letter': 'D'}, {'row': 5, 'letter': 'E'}, {'row': 6, 'letter': 'A'}, {'row': 6, 'letter': 'B'}, {'row': 6, 'letter': 'D'}, {'row': 6, 'letter': 'E'}, {'row': 7, 'letter': 'A'}, {'row': 7, 'letter': 'B'}, {'row': 7, 'letter': 'C'}, {'row': 7, 'letter': 'D'}, {'row': 7, 'letter': 'F'}, {'row': 8, 'letter': 'A'}, {'row': 8, 'letter': 'B'}, {'row': 8, 'letter': 'D'}, {'row': 8, 'letter': 'E'}, {'row': 8, 'letter': 'F'}, {'row': 9, 'letter': 'A'}, {'row': 9, 'letter': 'B'}, {'row': 9, 'letter': 'D'}, {'row': 9, 'letter': 'E'}, {'row': 9, 'letter': 'F'}, {'row': 10, 'letter': 'A'}, {'row': 10, 'letter': 'B'}, {'row': 10, 'letter': 'D'}, {'row': 10, 'letter': 'E'}, {'row': 10, 'letter': 'F'}, {'row': 11, 'letter': 'A'}, {'row': 11, 'letter': 'B'}, {'row': 11, 'letter': 'C'}, {'row': 11, 'letter': 'D'}, {'row': 11, 'letter': 'E'}, {'row': 11, 'letter': 'F'}]"
    ]
}

dict_flight_update_empty_example = {
    "departure_time": [
        "This field is required."
    ],
    "arrival_time": [
        "This field is required."
    ],
    "route": [
        "This field is required."
    ],
    "airplane": [
        "This field is required."
    ],
    "crew": [
        "This field is required."
    ],
    "price_economy": [
        "This field is required."
    ],
    "price_business": [
        "This field is required."
    ],
    "rows_economy_from": [
        "This field is required."
    ],
    "luggage_price_1_kg": [
        "This field is required."
    ]
}
