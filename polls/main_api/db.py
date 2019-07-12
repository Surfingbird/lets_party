import motor.motor_asyncio
import asyncio

def connect_db(host, port, db_name):
    client = motor.motor_asyncio.AsyncIOMotorClient(host, port)
    db = client[db_name]

    return db

host = 'localhost'
port = 27017
db_name = '12345'
conn = connect_db(host, port, db_name)