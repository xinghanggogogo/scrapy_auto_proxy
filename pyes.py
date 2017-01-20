# coding: utf-8 #

import pyes
from pyes.mappings import *

conn = pyes.ES(['127.0.0.1:9200'])

try:
    conn.indices.delete_index("test-index")
except:
    pass

conn.indices.create_index("test-index")

mapping = {
    u'parsedtext': {
        'boost': 1.0,
        'index': 'analyzed',
        'store': 'yes',
        'type': u'string',
        "term_vector": "with_positions_offsets"
    },
    u'name': {
        'boost': 1.0,
        'index': 'analyzed',
        'store': 'yes',
        'type': u'string',
        "term_vector": "with_positions_offsets"
    },
    u'title': {
        'boost': 1.0,
        'index': 'analyzed',
        'store': 'yes',
        'type': u'string',
        "term_vector": "with_positions_offsets"
    },
    u'position': {
        'boost': 1.0,
        'index': 'not_analyzed',
        'store': 'yes',
        'type': u'string'
    },
    u'uuid': {
        'boost': 1.0,
        'index': 'not_analyzed',
        'store': 'yes',
        'type': u'string'
    }
}

conn.indices.put_mapping("test-type", {'properties': mapping}, ["test-index"])
print('*')
conn.index({"name": "bourn", "parsedtext": "Joe Testere nice guy", "uuid": "11111", "position": "Beijing"}, "test-index", "test-type", 1)
print('**')
conn.default_indices=["test-index"]
print('***')
conn.indices.refresh()
print('****')

q = pyes.TermQuery("name", "bourn")
result = conn.search(q)
print('*****')

for item in result:

    print(item)
