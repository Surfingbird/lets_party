import motor.motor_asyncio
import asyncio
import aiohttp

# MongoDB
HOST = 'localhost'
PORT = 27017
DBNAME = 'kts'

client = None
db = None

def init_mongodb(host=HOST, port=PORT, dbname=DBNAME, loop=None):
    global client
    global db

    if loop is not None:
        client = motor.motor_asyncio.AsyncIOMotorClient(host, port, io_loop=loop)
    else:
        client = motor.motor_asyncio.AsyncIOMotorClient(host, port)

    db = client[dbname]

def print_status():
    print(type(client), client)
    print(type(db), db)

def get_mongo_conn():
    global db

    return db

#ES DB
scheme = "http://"
es_index = 'products'
es_type = 'product'
es_url = '127.0.0.1:9200'
main_url = scheme + es_url + "/" + es_index + "/" + es_type + "/"

es_session = aiohttp.ClientSession()
