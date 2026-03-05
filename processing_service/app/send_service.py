from processingService import ProcessingService
from logger import Logger
processin = ProcessingService()
logger = Logger.get_logger()

class SendService:
    def send_to_mongo_and_elastic(self, data: dict):
        processin.send_bysr_to_mangodb(data=data)
        processin.send_matadata_to_elastic(data=data)
