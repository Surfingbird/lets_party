import motor.motor_asyncio
from polls.models import db

def init_db(loop=None, host=db.HOST, port=db.PORT):
    if loop is not None:
        db.client = motor.motor_asyncio.AsyncIOMotorClient(host, port, io_loop=loop)
    else:
        db.client = motor.motor_asyncio.AsyncIOMotorClient(host, port)

    db.db = db.client[db.DBNAME]
    db.product_collection = db.db['products']
    db.profiles_collection = db.db['profiles']