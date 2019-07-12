import aiohttp

def smth():
    session = aiohttp.ClientSession()

    async with session.get('https://www.afisha.ru/msk/schedule_concert/') as resp:
        print(resp.status)
        print(await resp.text())

    await session.close()

smth()