from datetime import datetime
from elasticsearch_dsl import DocType, String, Date, Integer, Float
from elasticsearch_dsl.connections import connections

# Define a default Elasticsearch client
connections.create_connection(hosts=['localhost'])

class Extension(DocType):
    name = String()
    url = String()
    description = String()
    user_count = Integer()
    review_count = Float()
    review_score = Float()

    class Meta:
        index = 'exts'

# create the mappings in elasticsearch
Extension.init()

import json
exts = json.load(open('data/PAGES.json'))

# TODO source code extract

# rob query: all ext with this permission in manifest and this regex in source code
# https://www.elastic.co/guide/en/elasticsearch/guide/current/nested-query.html

for ext in exts:
    print(ext['name'])
    sources = extract_sources(ext['id'])
    # create and save
    ext = Extension(meta={'id': ext['ext_id']},
        name=ext['name'],
        sources=sources,
        url=ext['url'],
        review_count=ext['aggregateRating.properties.ratingCount'],
        review_score=ext['aggregateRating.properties.ratingValue'],
        description=ext['full_description'],
        user_count=int(ext['user_count']))
    ext.save()

# Display cluster health
print(connections.get_connection().cluster.health())