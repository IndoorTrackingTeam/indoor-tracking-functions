import os
import pymongo
# from dotenv import load_dotenv

# load_dotenv()
class Database:
    def __init__(self, collection):
        database = os.getenv('DB_NAME')

        self.connect(database, collection) 

    def connect(self, database, collection):
        try:
            url = os.getenv('DB_URL')
            self.cluster_connection = pymongo.MongoClient(
                url,
                tlsAllowInvalidCertificates=True 
            )
            self.db = self.cluster_connection[database] 
            self.collection = self.db[collection] 
            print('Connected to the database successfully!')
        except Exception as e:
            print('Error while trying to connect to the database')
