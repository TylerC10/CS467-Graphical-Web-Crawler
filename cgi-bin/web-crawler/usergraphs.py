#!/usr/bin/python

# Start main CGI logic
import cgi
import cgitb
import json
from d3helper import create_d3_tree_datastructure
cgitb.enable()

form = cgi.FieldStorage() 
# Get parameters in form submission
userId = form.getvalue('user_id')
searchCode = form.getvalue('search_code')

# Set database connection parameters
db_config = {
    'database': 'beginning_database',
    'user': 'copety',
    'password': 'eridanus',
    'host': 'firstdbinstance.cxvcjdies8vv.us-east-2.rds.amazonaws.com',
    'port': '5432'
}

# Create DB connection 
import psycopg2
conn = psycopg2.connect(**db_config)
cur = conn.cursor()

# Create reusable logic, if request contains a search_code then return full data search_code query for S3 
# Otherwise return a list of search_code associated with the user so he can pick one from the UI 
if searchCode:
    cur.execute("SELECT * FROM CRAWL.INFO WHERE search_code = %s;", [searchCode])
    usergraph = cur.fetchall()
    resulting_data = {}
    for row in usergraph:
        resulting_data['search_code'] = row[0]
        resulting_data['search_type'] = row[1]
        resulting_data['start_url'] = row[2]
        resulting_data['max_level'] = row[3]
        resulting_data['crawled_data_time'] = row[4].strftime("%b %d %Y %H:%M:%S")
    # Next get crawl data for the search_code 
    cur2 = conn.cursor()
    cur2.execute("SELECT * FROM CRAWL.DATA WHERE search_code = %s;", [searchCode])
    user_crawl_data = cur2.fetchall()
    resulting_link_data = []
    for row in user_crawl_data:
        resulting_link_data.append({'search_code': row[0],'id': row[1],'url': row[2],'level': row[3],'parent_id': row[4]})
    resulting_data['d3'] = create_d3_tree_datastructure(resulting_link_data)
    print("Content-Type: application/json\n")
    print(resulting_data)
else:
    # Generate user search_code list so he can select
    cur.execute("SELECT * FROM CRAWL.INFO WHERE search_code LIKE %s;", [userId + '%'])
    allusergraphs = cur.fetchall()
    resulting_data = []
    for row in allusergraphs:
        resulting_data.append({'search_code': row[0],'search_type': row[1],'start_url':row[2],'max_level':row[3],'crawled_data_time': row[4].strftime("%b %d %Y %H:%M:%S")})
    print("Content-Type: application/json\n")
    print(json.dumps(resulting_data))



