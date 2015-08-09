import re
from datetime import datetime
from subprocess import Popen, PIPE, STDOUT
from pymongo import Connection
from pymongo.errors import CollectionInvalid

HOST = 'us-apa1'
LOG_PATH = '/var/log/apache2/http-mydomain.com-access.log'
DB_NAME = 'mydb'
COLLECTION_NAME = 'apache_access'
MAX_COLLECTION_SIZE = 5 # in megabytes

def main():
    # connect to mongodb
    mongo_conn = Connection(HOST)
    mongo_db = mongo_conn[DB_NAME]
    try:
        mongo_coll = mongo_db.create_collection(COLLECTION_NAME,
                                                capped=True,
                                                size=MAX_COLLECTION_SIZE*1048576)
    except CollectionInvalid:
        mongo_coll = mongo_db[COLLECTION_NAME]

    # open remote log file
    cmd = 'ssh -f %s tail -f %s' % (HOST, LOG_PATH)
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)

    # parse and store data
    while True:
        line = p.stdout.readline()
        data = parse_line(line)
        data['time'] = convert_time(data['time'])
        mongo_coll.insert(data)

def parse_line(line):
    """Apache combined log format
    %h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\"
    """
    m = re.search(' '.join([
                r'(?P<host>(\d+\.){3}\d+)',
                r'.*',
                r'\[(?P<time>[^\]]+)\]',
                r'"\S+ (?P<url>\S+)',
                ]), line)
    if m:
        return m.groupdict()
    else:
        return {}

def convert_time(time_str):
    time_str = re.sub(r' -\d{4}', '', time_str)
    return datetime.strptime(time_str, "%d/%b/%Y:%H:%M:%S")

if __name__ == '__main__':
    main()
