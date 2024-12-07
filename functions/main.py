from datetime import datetime, timezone
import requests
import asyncio

from database.repositories.equipment_repository import EquipmentDAO
from database.repositories.router_data_repository import RouterDataDAO
from models.equipment_model import UpdateEquipmentsCurrentRoom, UpdateEquipmentsHistoric, NotificationBody
from utils.equipment_service import notify_all_users

url = 'https://run-machine-learning-api-prod-694723526996.us-east1.run.app/model-training/get-esp-position?esp_id='

async def update_equipments_location():
    try:
        equipmentDAO = EquipmentDAO()
        routerdataDAO = RouterDataDAO()
        all_esp = equipmentDAO.get_all_esp_id()

        # Updating each esp
        for esp in all_esp:
            print(esp['esp_id'])
            esp_data_exist = routerdataDAO.get_esp_id(esp_id=esp['esp_id'])
            print(esp_data_exist)
            if esp_data_exist != None:
                new_url = url + esp['esp_id']
                response = requests.get(new_url)

                if response.status_code == 200 and response.json() != "":
                    new_current_room = response.json()
                    equipment = equipmentDAO.get_current_room_and_date(esp['esp_id'])
                                    
                    if str(new_current_room) != str(equipment['c_room']):
                        date = datetime.now(timezone.utc)
                        update_database(equipmentDAO, new_current_room, esp['esp_id'], equipment, date)
                        notification_body = NotificationBody(equipment_name=equipment['name'], register_= equipment['register'], date=date, location=equipment['c_room'])
                        await notify_all_users(notification_body)
                    else:
                        print("It didn`t move")

                    equipmentDAO.update_current_date(esp['esp_id'])
                else:
                    if response.json() == "":
                        print(f'It wasn`t possible to get the room: {response.text}')
                    else:
                        print(f'Erro {response.status_code}: {response.text}')
                
    except Exception as e:
        print(f'Error when making the request: {e}')
        raise e

def update_database(equipmentDAO, new_current_room, esp_id, equipment, date):
    try:
        equipmentDAO.update_historic(UpdateEquipmentsHistoric(esp_id = esp_id, room = equipment['c_room'], initial_date = equipment['initial_date']['$date']))
        equipmentDAO.update_current_room(UpdateEquipmentsCurrentRoom(esp_id = esp_id, c_room = new_current_room), date)
            
    except Exception as e:
        print(f"Error when connecting with database: {e}")


if __name__ == "__main__":
    asyncio.run(update_equipments_location())