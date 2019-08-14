import motor.motor_asyncio
import asyncio
import aiohttp
import os

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

MONGO_HOST = 'MONGO_HOST'
MONGO_PORT = 'MONGO_PORT'
MONGO_DBNAME = 'MONGO_DBNAME'

LOCALHOST = 'localhost'
DEFAULT_MONGO_PORT = 27017
DEFAULT_DBNAME = 'kts'

def get_mongo_host():
    if MONGO_HOST in os.environ:
        host = os.environ.get(MONGO_HOST)

        return host
    else:
        return LOCALHOST

def get_mongo_port():
    if MONGO_PORT in os.environ:
        port = int(os.environ.get(MONGO_PORT))

        return port
    else:
        return DEFAULT_MONGO_PORT

def get_mongo_dbname():
    if MONGO_DBNAME in os.environ:
        dbname = os.environ.get(MONGO_DBNAME)

        return dbname
    else:
        return DEFAULT_DBNAME

# MongoDB
HOST: str = get_mongo_host()
PORT: int  = get_mongo_port()
DBNAME: str = get_mongo_dbname()

client: AsyncIOMotorClient = None
db: AsyncIOMotorDatabase = None

def init_mongodb(host=HOST, port=PORT, dbname=DBNAME, loop=None):
    global client
    global db

    if loop is not None:
        client = AsyncIOMotorClient(host, port, io_loop=loop)
    else:
        client = AsyncIOMotorClient(host, port)

    db = client[dbname]


def get_mongo_conn():
    global db

    return db

#ES DB
scheme: str = "http://"
es_index: str  = 'products'
es_type: str  = 'product'
es_url: str = '127.0.0.1:9200'

main_url: str = scheme + es_url + "/" + es_index + "/" + es_type + "/"

es_session = aiohttp.ClientSession()
