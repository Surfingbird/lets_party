import asyncio
from model import Profile


async def main():
    await Profile.objects.create(first_name = 'bbb', last_name = 'aaa')
    await Profile.objects.create(first_name = 'bbb', last_name = 'aaa')
    await Profile.objects.create(first_name = 'bbb', last_name = 'aaa')

    await Profile.objects.update(first_name = 'RRR')
    await Profile.objects.delete(first_name = 'RRR')


loop = asyncio.get_event_loop()
loop.run_until_complete(main())




