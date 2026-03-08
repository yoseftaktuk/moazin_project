from elasticsearch import Elasticsearch
import os
from logger.logger import Logger
logger = Logger.get_logger()

class ElasticService:
    def __init__(self):
        self.es = Elasticsearch(os.getenv('ELASTIC_URI'))
    def mapping(self):
        map = {
            'mappings':{
                'properties':{
                'meta_data':   {'type': 'object'},
                'audio_id' :   {'type': 'keyword'},
                'string': {'type': 'text'}
                    }
                }
            }
        return map         
        
    def create_index(self):
        if not self.es.indices.exists(index='audio'):
            response = self.es.indices.create(index='audio', body=self.mapping())
            logger.info(f'index create {response}')
            return
        return

    def upsert(self, data: dict):
        doc_id = data['audio_id']
        index_name = "audio"
        document_body = data
        response = self.es.index(
        index=index_name,
        id=doc_id,
        document=document_body
    )
        return response