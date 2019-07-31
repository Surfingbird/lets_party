from polls.models.fake_model_manager import *

fm = FakeModelManager()

async def main():
    await fm._create_fake_profiles(20)
    await fm._create_fake_products(200)   

loop = asyncio.get_event_loop()
loop.run_until_complete(main())