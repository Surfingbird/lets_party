import api
import random
import asyncio
import db

from faker import Faker

fake = Faker()

class FakeModelManager:
    def __init__(self):
        self.min_insts = 1
        self.max_insts = 10
        self.min_price = 50
        self.max_price = 100000

    async def _create_fake_products(self, count):
        products = []
        for i in range(count):
            product = api.create_product(fake.name(), fake.text(), \
             random.uniform(self.min_price, self.max_price), fake.url())
            products.append(product)

        await db.conn.test_collection.insert_many(products)

    async def _create_fake_profiles(self, count):
        profiles = []
        for i in range(count):

            
# m = FakeModelManager()

# loop = asyncio.get_event_loop()
# loop.run_until_complete(m._create_fake_products(10))