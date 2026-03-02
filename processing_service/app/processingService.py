from uuid import uuid4
from mongodb_connection import MongoDbService
from elastic_service import ElasticService
from logger import Logger
import speech_recognition as sr
logger = Logger.get_logger() 
mongo = MongoDbService()
elastic = ElasticService()

class ProcessingService:
    def add_id_for_data(self, data: dict):
        data['audio_id'] = str(uuid4())
        logger.info(f'id add to metadata')
        return data
    
    def add_audio_to_str_to_metadata(self, data: dict):
      try:
        r = sr.Recognizer()
        print(data)
        with sr.AudioFile(data['matadata']['path']) as source:
            audio = r.record(source)
        data['string'] = r.recognize_sphinx(audio).lower()   
        logger.info(f'convert audio to str') 
        return data 
      except sr.UnknownValueError as e:
          logger.error(str(e))
          raise str(e)

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
    
