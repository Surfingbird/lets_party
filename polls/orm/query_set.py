import motor.motor_asyncio

from polls.models.db import db
import asyncio

class QuerySet:
    def __init__(self, selector, collection):
        self.selector = selector
        self.collection = collection

        self.qs_limit = None
        self.qs_offset = 0

        # iterator
        self.data = None
        self.i = None
        self.length = None

    def filter(self, **selector):
        self.selector = {**self.selector, **selector}
        return self

    def limit(self, limit):
        self.qs_limit = int(limit)
        return self
    
    def offset(self, offset):
        self.qs_offset += int(offset)
        return self

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

    async def __aiter__(self):
        self.data = await db[self.collection].find(self.selector).skip(self.qs_offset).to_list(length=self.qs_limit)
        self.length = len(self.data)
        self.i = 0

        return self


    async def __anext__(self):
        if self.i < self.length:
            index = self.i
            self.i += 1

            return self.data[index]
        else:
            raise StopAsyncIteration 


    
    