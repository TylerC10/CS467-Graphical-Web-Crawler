#!/usr/bin/python

# Start main CGI logic
import cgi
import cgitb
cgitb.enable()

form = cgi.FieldStorage() 
# Get parameters in form submission
keyword = form.getvalue('stop_words')
searchType = form.getvalue('search_type')
startingUrl = form.getvalue('start_url')
userId = form.getvalue('user_id')
# Set general crawler parameters
db_config = {
    'database': 'beginning_database',
    'user': 'copety',
    'password': 'eridanus',
    'host': 'firstdbinstance.cxvcjdies8vv.us-east-2.rds.amazonaws.com',
    'port': '5432'
}

user_id = userId
# Get unique number for search_code 
import time
millis = int(round(time.time() * 1000))


# Perform the crawl
from search import WebCrawler
crawler = WebCrawler(db_config, user_id)
search_options = {
    'search_code': '%s-%s' % (user_id,millis), # Generate search_code as composite user and random millis time, needed to detect user in DB
    'search_type': searchType,# or 'BFS'
    'start_url': startingUrl, #'http://docs.peewee-orm.com/en/latest/peewee/querying.html',
    'max_level': 5,
    'persist': True
}
# Set response to JSON
print("Content-Type: text/html\n")

search_result = crawler.search(**search_options)
import json
# Create placeholder for links 
resulting_links = []
# Loop over search results and output each individual 'Link' object field
for link in search_result:
    resulting_links.append({'url':link.url, 'domain':link.domain, 'is_valid':link.is_valid, 'id':link.id, 'level':link.level})
# Set final response piece to resulting links
try:
    # Try to parse results as JSON, if this is valid then crawl was success
    json.dumps(resulting_links)
    print("<b class='bg-success'>Success</b>")
except Exception:
    # No need to throw error here, the crawler generated an error much earlier, so to the  browser anything else than a simple 'success' message is a 'stack error '
    pass 

    
