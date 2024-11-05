from datetime import datetime
import time
import requests
from zoneinfo import ZoneInfo

from database.repositories.equipment_repository import EquipmentDAO
from models.equipment_model import UpdateEquipmentsCurrentRoom, UpdateEquipmentsHistoric

url = 'https://run-machine-learning-api-prod-131050301176.us-east1.run.app/model-training/get-esp-position?esp_id='

def update_equipments_location():
    try:
        equipmentDAO = EquipmentDAO()

        all_esp = equipmentDAO.get_all_esp_id()

        for esp in all_esp:
            new_url = url + esp['esp_id']
            response = requests.get(new_url)

            print(f"response: {response.json()}")

            if response.status_code == 200 and response.json() != "":
                new_current_room = response.json()
                equipment = equipmentDAO.get_current_room_and_date(esp['esp_id'])
                if str(new_current_room) != str(equipment['c_room']):
                    update_database(equipmentDAO, new_current_room, esp['esp_id'], 0)
                else:
                    print("It didn`t move")
            else:
                if response.json() == "":
                    print(f'It wasn`t possible to get the room: {response.text}')
                else:
                    print(f'Erro {response.status_code}: {response.text}')
                
    except Exception as e:
        print(f'Error when making the request: {e}')

def update_database(equipmentDAO, new_current_room, esp_id, num_try):
    num_try += 1
    try:
        date = datetime.now()
        date_key = date.strftime("%Y-%m-%d %H:%M:%S")

        equipmentDAO.update_historic(UpdateEquipmentsHistoric(esp_id = esp_id, room = new_current_room, initial_date = date_key))
        equipmentDAO.update_current_room(UpdateEquipmentsCurrentRoom(esp_id = esp_id, c_room = new_current_room), date_key)
            
    except Exception as e:
        print(f"Error when connecting with database: {e}")
        
update_equipments_location()