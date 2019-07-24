from query_set import QuerySet
import asyncio

class Manage:
    def __init__(self):
        self.model_cls = None

    async def create(self):
        print("__create__")
        await asyncio.sleep(0)
        
        pass

    def filter(self, **selector):
        return QuerySet(selector)

    async def update(self):
        print("__update__")
        await asyncio.sleep(0)

        pass

    async def delete(self):
        print("__delete__")
        await asyncio.sleep(0)

        pass