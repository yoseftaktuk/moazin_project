from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
import gridfs
from logger.logger import Logger
logger = Logger.get_logger() 

host = os.getenv('HOST')
port = os.getenv('PORT')
user = os.getenv('USER')
password = os.getenv('PASSWORD')
uri = f"mongodb://{user}:{password}@{host}:{port}"
print(uri)

class MongoDbService:
    def __init__(self):
        self.client = None
        self.db = None
        self.colletion = None
    def conect(self):
        try:
            self.client = MongoClient(uri)
            self.client.admin.command('ping')  
            logger.info('connection to mongodb')
        except ConnectionFailure as e:
            logger.error(str(e))
            raise str(e)
        
    def creat_collection(self):
        try:
            self.db = self.client['my_db']
            self.colletion = self.db['my_collection']
            self.fs = gridfs.GridFS(self.db)
            logger.info('collection creat')
            return self.colletion  
        except ConnectionError as e:
            logger.error(str(e))
            raise str(e)

    def insert_one_preparing(self,byts_data, item: dict):
        result = self.fs.put(byts_data, filename=item['matadata']['name'],
        audio_id=item['audio_id'],
        metadata=item['matadata'])
        logger.info('data save in mongo db')
        return result

    def get_the_file(self, path):
        try:
            with open(path, 'rb') as f:
                data = f.read()
                return data 
        except FileNotFoundError as e:
            logger.error(str(e))
            raise str(e)    