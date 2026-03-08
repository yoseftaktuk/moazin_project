from fastapi import APIRouter, HTTPException
from elastic_query import ElasticQuery
from logger.logger import Logger
from redis_connection import RedisService
redis = RedisService()
logger = Logger.get_logger() 
query = ElasticQuery()
route = APIRouter()

@route.get('/get_all')
def get_all():
    try:
        if redis.get_from_redis('get_all'):
            return redis.get_from_redis('get_all')
        logger.info("The sending was successful.") 
        redis.send_to_redis('get_all', query.get_all())
        return query.get_all()
    except HTTPException as e:
        logger.error('The sending failed.')
        raise str(e)  

@route.get('/get_by_word/{word}')
def get_by_word(word: str):
    try:
        if redis.get_from_redis(f'get_by_word/{word}'):
            return redis.get_from_redis(f'get_by_word/{word}')
        logger.info("The sending was successful.") 
        redis.send_to_redis(f'get_by_word/{word}', query.get_by_word(word=word))
        return query.get_by_word(word=word)
    except HTTPException as e:
        logger.error('The sending failed.')
        raise str(e)      
    
@route.get('/get_top_5_bds_percent')
def get_top_5_bds_percent():
    try:
        if redis.get_from_redis('get_top_5_bds_percent'):
            return redis.get_from_redis('get_top_5_bds_percent')
        result = query.get_top_5_bds_percent()
        redis.send_to_redis('get_top_5_bds_percent', result)
        logger.info("The sending was successful.") 
        return result
    except HTTPException as e:
        logger.error('The sending failed.')
        raise str(e)      

@route.get('/get_all_high_bds_threat_level')
def get_all_high_bds_threat_level():
    try:
        if redis.get_from_redis('get_top_5_bds_percent'):
            return redis.get_from_redis('get_all_high_bds_threat_level')
        result = query.get_all_high_bds_threat_level()
        redis.send_to_redis('get_all_high_bds_threat_level', value=result)
        logger.info("The sending was successful.")
        return result
    except HTTPException as e:
        logger.error('The sending failed.')
        raise str(e)   
    
@route.get('/get_all_is_bds')
def search_by_words():
    try:
       if redis.get_from_redis('get_top_5_bds_percent'):
           return redis.get_from_redis('get_top_5_bds_percent')
       result = query.get_all_is_bds() 
       redis.send_to_redis('get_top_5_bds_percent', value=result)
       logger.info("The sending was successful.")
       return result    
    except HTTPException as e:
        logger.error('The sending failed.')
        raise str(e)   
    