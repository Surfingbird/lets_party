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
        self.min_price = 300
        self.max_price = 100000

        self.max_id = 1000

    def _create_list_fake_insts(self):
        count = random.randint(self.min_insts, self.max_insts)
        insts = []
        idx = set()

        for i in range(count):
            price = random.uniform(self.min_price, self.max_price)

            _id = 0
            while True:
                _id = random.randint(1, self.max_id)
                if _id not in idx:
                    idx.add(_id)
                    break

            inst = api.create_instance(_id, fake.word(), fake.word(), price, fake.word())
            insts.append(inst)

        return insts


    async def _create_fake_events(self, count):
        events = []
        for i in range(count):
            insts = self._create_list_fake_insts()
            event = api.create_event(fake.name(), fake.text(), insts)
            events.append(event)

        await db.conn.test_collection.insert_many(events)

            
# m = ModelManager()

# loop = asyncio.get_event_loop()
# loop.run_until_complete(m._create_fake_events(10))