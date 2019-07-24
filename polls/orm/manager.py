from query_set import QuerySet
import asyncio
import inspect 

from db import db

class Manage:
    def __init__(self):
        self.model_cls = None


    def __get__(self, instance, owner):
        if self.model_cls is None:
            self.model_cls = owner

        return self


    async def create(self, **kwargs):
        obj = self.model_cls(**kwargs)
        await obj.save()


    def filter(self, **selector):
        return QuerySet(selector, self.model_cls.collection)


    async def update(self, **kwargs):
        for key, value in kwargs.items():
            self.model_cls.__dict__[key].validate(value)

        collection  = self.model_cls.Meta.collection_name
        await db[collection].update_many({}, { '$set' : kwargs})


    async def delete(self, **kwargs):
        for key, value in kwargs.items():
            self.model_cls.__dict__[key].validate(value)

        collection  = self.model_cls.Meta.collection_name
        await db[collection].delete_many(kwargs)