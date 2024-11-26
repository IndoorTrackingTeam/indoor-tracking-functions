import json
from bson import json_util
from datetime import datetime

from database.config_db import Database
from models.equipment_model import UpdateEquipmentsHistoric, UpdateEquipmentsCurrentRoom

class EquipmentDAO:
    def __init__(self):
        self.db = Database(collection='equipment')

    def get_all_esp_id(self):
        try:
            res = self.db.collection.find({}, {'_id': 0, 'esp_id': 1} )

            parsed_json = json.loads(json_util.dumps(res))
            return parsed_json
        
        except Exception as e:
            print(f'There was an error trying to get the equipment: {e}')
            return None
        
    def get_current_room_and_date(self, esp_id):
        try:
            res = self.db.collection.find_one({'esp_id': esp_id},  {'_id': 0, 'name': 1, 'register': 1,  'c_room': 1, 'initial_date': 1})
            parsed_json = json.loads(json_util.dumps(res))
            
            return parsed_json
        except Exception as e:
            print(f'There was an error trying to get equipment: {e}')
            return None
        
        
    def update_historic(self, equipment_data: UpdateEquipmentsHistoric):
        try:
            res = self.db.collection.update_one({'esp_id': equipment_data.esp_id}, {'$push': {'historic': equipment_data.model_dump(exclude='esp_id')}})

            if res.matched_count == 0:
                return False
            else:
                return True
        except Exception as e:
            print(f'There was an error trying to update equipment maintenance: {e}')
            return None
        
    
    def update_current_room(self, equipment_data: UpdateEquipmentsCurrentRoom, date):
        try:
            res = self.db.collection.update_one({'esp_id': equipment_data.esp_id},{'$set': {'c_room': equipment_data.c_room, 'initial_date': date}})

            if res.matched_count == 0:
                return False
            else:
                return True
        except Exception as e:
            print(f'There was an error trying to update equipment\'s current room: {e}')
            return None
        
    def update_current_date(self, esp_id: str):
        try:
            date = datetime.now()

            res = self.db.collection.update_one({'esp_id': esp_id},{'$set': {'c_date': date}})

            if res.matched_count == 0:
                return False
            else:
                return True
        except Exception as e:
            print(f'There was an error trying to update equipment\'s current data(last time updated): {e}')
            return None
        
    
        