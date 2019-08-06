import asyncio
import inspect 
import bson

from pymongo.results import DeleteResult, UpdateResult

from polls.models.db import db, get_mongo_conn
from polls.orm.query_set import QuerySet
from bson.objectid import ObjectId

class Manage:
    def __init__(self):
        self.model_cls = None

# ВОПРОС!
    def __get__(self, instance, owner):
        # if self.model_cls is None:
        self.model_cls = owner

        return self


    async def create(self, **kwargs):
        obj = self.model_cls(**kwargs)
        await obj.save()


    async def get(self, **kwargs) -> dict:
        collection  = self.model_cls.Meta.collection_name
        selector = dict()

        for key, value in kwargs.items():
            self.model_cls.__dict__[key].validate(value)
            
            if key == '_id':
                try:
                    selector[key] = ObjectId(value)
                except bson.errors.InvalidId:
                    raise

            else:
                selector[key] = value

        db = get_mongo_conn()
        data = await db[collection].find_one(selector)
        if data is not None:
            data['_id'] = str(data['_id'])

        return data


    def filter(self, **selector) -> QuerySet:
        collection  = self.model_cls.Meta.collection_name
        return QuerySet(selector, collection)


    async def update(self, **kwargs) -> UpdateResult:
        for key, value in kwargs.items():
            self.model_cls.__dict__[key].validate(value)

        collection  = self.model_cls.Meta.collection_name
        db = get_mongo_conn()

        await db[collection].update_many({}, { '$set' : kwargs})


    async def delete(self, **kwargs) -> DeleteResult:
        for key, value in kwargs.items():
            self.model_cls.__dict__[key].validate(value)

        collection  = self.model_cls.Meta.collection_name
        db = get_mongo_conn()

        await db[collection].delete_many(kwargs)

    async def count(self) -> int:
        collection: str  = self.model_cls.Meta.collection_name
        db = get_mongo_conn()

        n: int  = await db[collection].count_documents({})

        return n