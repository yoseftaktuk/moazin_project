import os
from pathlib import Path
import pathlib
import datetime
from prudocer import KafkaService
kafka = KafkaService()


class DataService:
    def __init__(self):
        self.PATH = 'data/podcasts/'
    def loop_in_file(self):
        directory = os.fsencode(self.PATH)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith('.wav'):
                filename = self.PATH + filename 
                p = Path(filename)
                matadata = self.get_meta_data(p)
                kafka.send_to_kafka(topic='first_topic', data={'matadata': matadata,
                                     'audio_byts': self.audio_to_byts(filename)})

    def get_meta_data(self, data: pathlib._local.WindowsPath):
        return {'name': data.name,
                'size': data.stat().st_size,
                'time': datetime.datetime.now()}
    
    def audio_to_byts(self, path: str):
        with open(path, 'rb') as f:
            return f.read()

a = DataService()
a.loop_in_file('data/podcasts/')

       