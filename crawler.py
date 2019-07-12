import asyncio
import aiohttp
import random
import logging

class LimitedQueue:
    def __init__(self, limit):
        self.limit = limit
        self.q = asyncio.Queue()
        
    async def put(self, path):
        await self.q.put(path)

    async def get(self):
        return await self.q.get()

    

class Crawler:
    def __init__(self, root_url, max_rps, workers_count):
        self.workers_count = 10
        self.max_rps = 10
        self.q = asyncio.Queue()
        self.seen_urls = set()
        self.session = None

        self.q.put_nowait(root_url)
        logging.basicConfig(level = logging.DEBUG)

        logging.info(u'Crawler was init')

    async def do_work(self, idx):
        logging.info(f'worker {idx} was started')

        while True:
            path = await self.q.get()



    async def connection(self):
        self.session = await aiohttp.ClientSession()

    async def disconnection(self):
        await self.session.close()
        
    async def crawl(self):
        await asyncio.gather(*(self.do_work(n) for n in range(self.workers_count)))

root_url = 'qwe'
max_rps = 10
workers_count = 10

crawler = Crawler(root_url, max_rps, workers_count)

loop = asyncio.get_event_loop()
loop.run_until_complete(crawler.crawl())