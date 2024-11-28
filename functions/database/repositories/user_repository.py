from database.config_db import Database
import json
from bson import json_util

class UserDAO: # DAO - Data Access Object
    def __init__(self):
        self.db = Database(collection='user')

    def get_users_emails(self):
        try:
            result = self.db.collection.find({}, {'_id': 0, 'email': 1})
            data_json = json.loads(json_util.dumps(result))

            return data_json
        except Exception as e:
            print(f'There was an error when trying to get user: {e}')
            return False
    
    