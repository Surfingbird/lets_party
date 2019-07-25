import motor.motor_asyncio

from db import db
import asyncio

class QuerySet:
    def __init__(self, selector, collection):
        self.selector = selector
        self.collection = collection

        self.qs_limit = None
        self.qs_offset = 0

    def filter(self, **selector):
        self.selector = {**self.selector, **selector}

    def limit(self, limit):
        self.qs_limit = limit
    
    def offset(self, offset):
        self.qs_offset = offset

    def __getitem__(self, item):
        if isinstance(item, slice):
            if item.step is not None:
                raise NotImplementedError

            if item.start is not None and item.stop is not None:
                self.qs_limit = item.stop - item.start - 1

            if item.start is not None:
                self.qs_offset += item.start
        
            return self

        else:
            raise TypeError
        
        
    async def __await__(self):
        data = await db[self.collection].find(self.selector).skip(self.qs_offset).to_list(length=self.qs_limit)

        return data