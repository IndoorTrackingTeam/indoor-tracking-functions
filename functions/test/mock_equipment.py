from datetime import datetime

def create_valid_equipments():
    return [
        {
            "name": "Multi Parameter Monitor",
            "register": "PAT1111",
            "maintenance": False,
            "c_room": "Emergency",
            "c_date": datetime(2024,8,8,19,54,14),
            "initial_date": datetime(2024,8,8,19,54,14),
            "esp_id": "1111",
            "historic": [
                {
                    "initial_date": datetime(2024,8,5,8,0,0),
                    "room": "Room 20"
                },
                {
                    "initial_date": datetime(2024,8,7,15,34,14),
                    "room": "Clinic"
                },
                {
                    "initial_date": datetime(2024,8,7,22,12,16),
                    "room": "Room 14"
                }
            ]
        },
        {
            "name": "Defibrillator",
            "register": "PAT2222",
            "maintenance": False,
            "c_room": "Emergency",
            "c_date": datetime(2024,8,8,19,54,14),
            "initial_date": datetime(2024,8,8,19,54,14),
            "esp_id": "2222"
        },
        {
            "name": "Infusion Pump",
            "register": "PAT3333",
            "maintenance": True,
            "c_room": "Maintenance room",
            "c_date": datetime(2024,8,8,19,54,14),
            "initial_date": datetime(2024,8,8,19,54,14),
            "esp_id": "3333"
        }
    ]