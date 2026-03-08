import redis
import os 
import json

host = os.getenv('REDIS_HOST') 
class RedisService:
    def __init__(self):
        self.r = redis.Redis(host=host, port=6379, db=0)   

    def pop_from_q(self,key: str): 
        data = self.r.brpop(key) 
        data = json.loads(data[1].decode('utf-8'))
        return data     
    
    def get_from_redis(self, key):
        item = self.r.get(key) 
        if item:
            return json.loads(item)
        return False  

    def send_to_redis(self, key, value):
        self.r.set(name=key, value=json.dumps(value, default=str), ex=50)