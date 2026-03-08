from fastapi import APIRouter, HTTPException
from elastic_query import ElasticQuery
from logger.logger import Logger
logger = Logger.get_logger() 
query = ElasticQuery()
route = APIRouter()

@route.get('/get_all')
def get_all():
    try:
        logger.info("The sending was successful.") 
        return query.get_all()
    except HTTPException as e:
        logger.error('The sending failed.')
        raise str(e)  

@route.get('/get_by_word/{word}')
def get_by_word(word: str):
    try:
        logger.info("The sending was successful.") 
        return query.get_by_word(word=word)
    except HTTPException as e:
        logger.error('The sending failed.')
        raise str(e)      
    
@route.get('/get_top_5_bds_percent')
def get_top_5_bds_percent():
    try:
        logger.info("The sending was successful.") 
        return query.get_top_5_bds_percent()['aggregations']
    except HTTPException as e:
        logger.error('The sending failed.')
        raise str(e)      

@route.get('/get_all_high_bds_threat_level')
def get_all_high_bds_threat_level():
    try:
        logger.info("The sending was successful.")
        return query.get_all_high_bds_threat_level()
    except HTTPException as e:
        logger.error('The sending failed.')
        raise str(e)   
    
@route.get('/get_all_is_bds')
def search_by_words():
    try:
       logger.info("The sending was successful.")
       return query.get_all_is_bds()    
    except HTTPException as e:
        logger.error('The sending failed.')
        raise str(e)   
    