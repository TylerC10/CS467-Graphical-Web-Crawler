from search import WebCrawler


db_config = {
    'database': 'beginning_database',
    'user': 'copety',
    'password': 'eridanus',
    'host': 'firstdbinstance.cxvcjdies8vv.us-east-2.rds.amazonaws.com',
    'port': '5432'
}

user_id = '123456'
crawler = WebCrawler(db_config, user_id)

search_options = {
    'search_code': '198765',
    'search_type': 'BFS', # or 'BFS'
    'start_url': 'http://docs.peewee-orm.com/en/latest/peewee/querying.html',
    'max_level': 2,
    'persist': True
}
search_result = crawler.search(**search_options)

print '---------------------------'
print 'RESULTS'
print '---------------------------'
print '\n'.join([str(x) for x in search_result])
print '---------------------------'
print 'TOTAL RESULTS: %s' %len(search_result)
