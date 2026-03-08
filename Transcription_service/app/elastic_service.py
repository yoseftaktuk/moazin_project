from elasticsearch import Elasticsearch
import os
from logger.logger import Logger
logger = Logger.get_logger()

class ElasticService:
    def mapping(self):
        map = {
            'mappings':{
                'properties':{
                'meta_data':   {'type': 'object'},
                'audio_id' :   {'type': 'keyword'}
                    }
                }
            }
        return map         
        
    def create_index(self):
        es = Elasticsearch(os.getenv('ELASTIC_URI',"http://elasticsearch:9200"))  
        if not es.indices.exists(index='audio'):
            response = es.indices.create(index='audio', body=self.mapping())
            logger.info(f'index create {response}')
            return
        return

    def upsert(self, data: dict):
        es = Elasticsearch(os.getenv('ELASTIC_URI',"http://elasticsearch:9200"))
        doc_id = data['audio_id']
        index_name = "audio"
        document_body = data
        response = es.index(
        index=index_name,
        id=doc_id,
        document=document_body
    )
        return response