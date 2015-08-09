import time
from datetime import datetime, timedelta
from pymongo import Connection

DB_NAME = 'mydb'
COLLECTION_NAME = 'apache_access'

def main():
    # connect to mongodb
    mongo_conn = Connection('nosat')
    mongo_db = mongo_conn[DB_NAME]
    mongo_coll = mongo_db[COLLECTION_NAME]

    # find the number of requests in the last minute
    while True:
        d = datetime.now() - timedelta(seconds=60)
        N_requests = mongo_coll.find({'time': {'$gt': d}}).count()
        print 'Requests in the last minute:',  N_requests
        time.sleep(2)

if __name__ == '__main__':
    main()
