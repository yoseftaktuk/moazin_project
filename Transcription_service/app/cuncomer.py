from logger.logger import Logger
from kafka import KafkaConsumer
import json
import time
import os
from prudocer import KafkaService
from elastic_service import ElasticService
from transcription_service import TranscriptionService
transcription = TranscriptionService()
elastic = ElasticService()
logger = Logger.get_logger() 
kafka = KafkaService()
kafka_uri = os.getenv('KAFKA_URI')

def get_from_kafka(topic: str):
    while True:
        try:
            consumer = KafkaConsumer(
                topic,
                group_id = '2',
                bootstrap_servers=kafka_uri,
                auto_offset_reset='earliest',
                enable_auto_commit=False,
                max_poll_interval_ms=600000,
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )
            logger.info("Connected to Kafka") 
            break
        except Exception:
            logger.error("Waiting for Kafka...")
            time.sleep(2)
    while True:        
        records = consumer.poll(timeout_ms=1000)        
        for tp, messages in records.items():
            for message in messages:
                data = message.value
                transcription.add_audio_to_str_to_metadata(data=data)# convert audio to string and add the str to data dict 
                data['audio_id'] = hash(str(data['matadata']['name']) + str(data['matadata']['size']) + str(data['matadata']['time']) + str(data['matadata']['path']))
                elastic.create_index()
                elastic.upsert(data) #update the elastic index
                kafka.send_to_kafka(topic='secend_topic', data=data)
       
        if records:
           consumer.commit_async()     