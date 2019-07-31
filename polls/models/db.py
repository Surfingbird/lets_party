import motor.motor_asyncio
import asyncio
import aiohttp

# MONGODB
HOST = 'localhost'
PORT = 27017
DBNAME = 'kts_orm'

client = None
db = None

product_collection = None
profiles_collection = None

#ES DB
scheme = "http://"
es_index = 'products'
es_type = 'product'
es_url = '127.0.0.1:9200'
main_url = scheme + es_url + "/" + es_index + "/" + es_type + "/"

es_session = aiohttp.ClientSession()
