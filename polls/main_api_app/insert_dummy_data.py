from polls.models.fake_model_manager import *
from polls.models.db import init_mongodb

fm = FakeModelManager()

async def main():
    init_mongodb()
    await fm._create_fake_profiles(20)
    await fm._create_fake_products(200)   

loop = asyncio.get_event_loop()
loop.run_until_complete(main())