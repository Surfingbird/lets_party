import motor.motor_asyncio
import asyncio
import aiohttp

# MongoDB
host = 'localhost'
port = 27017
db_name = '12345'

client = motor.motor_asyncio.AsyncIOMotorClient(host, port)
conn = client[db_name]

product_collection = conn['products']
profiles_collection = conn['profiles']

#ES DB
scheme = "http://"
es_index = 'products'
es_type = 'product'
es_url = '127.0.0.1:9200'
main_url = scheme + es_url + "/" + es_index + "/" + es_type + "/"

es_session = aiohttp.ClientSession()
