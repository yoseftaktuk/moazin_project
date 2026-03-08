import os
from pathlib import Path
import pathlib
import datetime
from prudocer import KafkaService
from logger.logger import Logger
from uuid import uuid4
kafka = KafkaService()
logger = Logger.get_logger() 

class DataService:
    def __init__(self):
        self.PATH = 'data/'
    def loop_in_file(self):
        directory = os.fsencode(self.PATH)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith('.wav'):
                filename = self.PATH + filename 
                p = Path(filename)
                matadata = self.get_meta_data(p, filename)
                kafka.send_to_kafka(topic='first_topic', data={'matadata': matadata})
                
    def get_meta_data(self, data, path):
        return {'name': data.name,
                'size': data.stat().st_size,
                'time': datetime.datetime.now(),
                'path': path}
    def add_id_for_data(self):
        logger.info(f'id add to metadata')
        return str(uuid4())



       