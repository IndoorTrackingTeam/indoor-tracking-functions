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
            print(f'Updating location of ESP {esp["esp_id"]}')
            new_url = url + esp['esp_id']
            response = requests.get(new_url)

            if response.status_code == 200:
                update_database(equipmentDAO, response.json(), esp['esp_id'], 0)
            else:
                print(f'Erro {response.status_code}: {response.text}')
                
    except Exception as e:
        print(f'Error when making the request: {e}')

def update_database(equipmentDAO, new_current_room, esp_id, num_try):
    num_try += 1
    try:
        sp_tz = ZoneInfo("America/Sao_Paulo")

        date = datetime.now(sp_tz)
        date_key = date.strftime("%Y-%m-%d %H:%M:%S")

        equipmentDAO.update_historic(UpdateEquipmentsHistoric(esp_id = esp_id, room = new_current_room, initial_date = date_key))
        equipmentDAO.update_current_room(UpdateEquipmentsCurrentRoom(esp_id = esp_id, c_room = new_current_room), date_key)
        print(f'Location of ESP {esp_id} updated successfully')
            
    except Exception as e:
        print(f"Error when connecting with database: {e}")
        
update_equipments_location()