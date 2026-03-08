from uuid import uuid4
from mongodb_connection import MongoDbService
from elastic_service import ElasticService
from logger.logger import Logger
logger = Logger.get_logger() 
mongo = MongoDbService()
elastic = ElasticService()

class ProcessingService:

    def send_matadata_to_elastic(self, data: dict):
        try:
            elastic.create_index()
            elastic.upsert(data)
            logger.info('data save im mongodb')
            return data
        except ConnectionError as e:
            logger.error(str(e))
            raise str(e)

    def send_bysr_to_mangodb(self, data: dict):
        mongo.conect()
        mongo.creat_collection()
        bytes_data = mongo.get_the_file(data['matadata']['path'])
        mongo.insert_one_preparing(bytes_data, data)
        return data
    
