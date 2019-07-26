import random
import asyncio

from faker import Faker
from polls.models.orm_models import Product, Profile


fake = Faker()

class FakeModelManager:
    def __init__(self):
        self.min_insts = 1
        self.max_insts = 10
        self.min_price = 50
        self.max_price = 100000
        self.max_id = 99999999


    async def _create_fake_profile(self):
        profile = Profile(vk_id=random.randint(self.min_price, self.max_price),
                first_name = fake.name(),
                last_name = fake.name(),
                photo_url = fake.url()
            )

        await profile.save()

        return profile

    async def _create_fake_profiles(self, count):
        for _ in range(count):
            await self._create_fake_profile()


    async def _create_fake_product(self):
        product = Product(product_name=fake.name(),
            discription = fake.text(),
            price = random.randint(self.min_price, self.max_price),
            img_url = fake.url(),
            product_url = fake.url()
        )

        await product.save()

        return product

    async def _create_fake_products(self, count):
        for _ in range(count):
            await self._create_fake_product()