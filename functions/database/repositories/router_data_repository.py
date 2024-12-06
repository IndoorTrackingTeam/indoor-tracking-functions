import json
from bson import json_util

from database.config_db import Database

class RouterDataDAO:
    def __init__(self):
        self.db = Database(collection='router-data')

    def get_esp_id(self, esp_id):
        try:
            res = self.db.collection.find_one({'esp_id': esp_id}, {'_id': 0, 'esp_id': 1} )
            print(f'esp: {res}')
            parsed_json = json.loads(json_util.dumps(res))
            return parsed_json
        
        except Exception as e:
            print(f'There was an error trying to get the equipment: {e}')
            return None