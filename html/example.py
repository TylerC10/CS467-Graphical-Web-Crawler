from search import WebCrawler
import cgi, cgitb


db_config = {
    'database': 'postgres',
    'user': 'postgres',
    'password': 'postgres',
    'host': '127.0.0.1',
    'port': '5432'
}

user_id = '123456'
crawler = WebCrawler(db_config, user_id)

data = cgi.FieldStorage()
search_options = {
    'search_code': '098765',
    'search_type': data["search_type"].value,
    'start_url': data["starting_url"].value,
    'max_level': 2,
    'stop_words': data["stop_words"].value,
    'persist': True
}
search_result = crawler.search(**search_options)

print '---------------------------'
print 'RESULTS'
print '---------------------------'
print '\n'.join([str(x) for x in search_result])
print '---------------------------'
print 'TOTAL RESULTS: %s' %len(search_result)
