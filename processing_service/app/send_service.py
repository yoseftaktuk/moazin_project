from processingService import ProcessingService
from logger import Logger
processin = ProcessingService()
logger = Logger.get_logger()

class SendService:
    def send_to_mongo_and_elastic(self, data: dict):
        processin.add_id_for_data(data=data)
        processin.add_audio_to_str_to_metadata(data)
        processin.send_bysr_to_mangodb(data=data)
        processin.send_matadata_to_elastic(data=data)
