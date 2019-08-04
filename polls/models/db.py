import motor.motor_asyncio
import asyncio
import aiohttp

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

# MongoDB
HOST: str = 'localhost'
PORT: int  = 27017
DBNAME: str = 'kts'

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
