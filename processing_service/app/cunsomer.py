from logger import Logger
from kafka import KafkaConsumer
import json
import time
import os
from prudocer import KafkaService
from processingService import ProcessingService
from send_service import SendService
logger = Logger.get_logger() 
kafka = KafkaService()
processing = ProcessingService()
kafka_uri = os.getenv('KAFKA_URI')
send = SendService()
def get_from_kafka(topic: str):
    while True:
        try:
            consumer = KafkaConsumer(
                topic,
                group_id = '1',
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
                send.send_to_mongo_and_elastic(data=data)
        
        if records:
           consumer.commit_async()        
