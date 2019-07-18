import motor.motor_asyncio
import asyncio

host = 'localhost'
port = 27017
db_name = '12345'

client = motor.motor_asyncio.AsyncIOMotorClient(host, port)
conn = client[db_name]

product_collection = conn['products']
profiles_collection = conn['profiles']
