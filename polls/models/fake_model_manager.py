import api
import random
import asyncio
from polls.models import db

from faker import Faker

fake = Faker()

class FakeModelManager:
    def __init__(self):
        self.min_insts = 1
        self.max_insts = 10
        self.min_price = 50
        self.max_price = 100000
        self.max_id = 99999999

    async def _create_fake_products(self, count):
        products = []
        for i in range(count):
            product = api.create_product(fake.name(), fake.text(), \
             random.uniform(self.min_price, self.max_price), fake.url())
            products.append(product)

        res = await db.product_collection.insert_many(products)
        if res is None:
            return False

        return True


    async def _create_fake_profiles(self, count):
        profiles = []
        idxs = set()

        for i in range(count):
            uid = 0
            while True:
                idx = random.randint(1, self.max_id)
                if idx not in idxs:
                    idxs.add(idx)
                    uid = idx
                    break

            first_name = fake.name()
            last_name = fake.name()
            photo_url = fake.url()
            wishes = []
            intentions = []

            profile = {
                'uid' : uid,
                'first_name' : first_name,
                'last_name' : last_name,
                'photo_url' : photo_url,
                'wishes' : wishes,
                'intentions' : intentions
            }
            profiles.append(profile)

        res = await db.profiles_collection.insert_many(profiles)
        if res is None:
            return False

        return True