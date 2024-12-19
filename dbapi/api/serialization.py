import json

def queryToJSON(query: str):
   jsonQuery = "with data AS \n ({query}) \n \
      SELECT to_jsonb(data) as result from data;" \
      .format(query=query)
   return jsonQuery

def deserializeTags(data):
    result = []
    if data:
      for row in data:
         row_dict = dict(row)
         if 'tags' in row:
            row_dict['tags'] = json.loads(row['tags'])
         result.append(row_dict)
    return result
