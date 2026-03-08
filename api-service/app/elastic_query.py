from elastic_service import ElasticService

elastic = ElasticService()

class ElasticQuery:
    def get_all(self):
        query = {'size':100,
"query": {
"match_all": {}
}
}
        return elastic.query(query)['hits']
    
    def get_by_word(self, word):
        query = {"query": {"match": {"string": word}}} 
        return elastic.query(query=query)
    
    def get_top_5_bds_percent(self):
        query = {
  "size": 0,
  "aggs": {
    "top_bds_percent": {
      "top_hits": {
        "size": 5,
        "sort": [
          {
            "bds_percent": {
              "order": "desc"
            }
          }
        ]
      }
    }
  }
}
        return elastic.query(query=query)['aggregations']
    
    def get_all_high_bds_threat_level(self):
        query = {"size": 100,
            'query':
            {'match':
             {'bds_threat_level': 'HIGH'}
             }
             }
        return elastic.query(query=query)['hits']
    
    def get_all_is_bds(self):
        query = { 
    'query': { 
        'bool': { 
            'must': [  
                { 'term': { 'is_bds':  'true' } } 
            ] 
        } 
    } ,
        "sort": [
          {
            "bds_percent": {
              "order": "desc"
            }
          }
        ]
} 
        return elastic.query(query=query)['hits']