import asyncio
import aiohttp
import aio_pika
import json
import time

from bs4 import BeautifulSoup
from urllib.parse import urlparse
from collections import deque

from polls.models.db import init_mongodb, DBNAME

import re

import polls.models.model_manager as model_manager
import polls.models.db as db
from  polls.models.orm_models import Product
from polls.main_api_app.elastick_client import ElastickClient

mm = model_manager.ModelManager()
es_client = ElastickClient()
es_client.connect()
        
NSEC_IN_SEC = 10 ** 9
COUNT = 10

class Crawler:
    def __init__(self, root_url, max_rps, workers_count):
        self.workers_count = workers_count
        self.max_rps = max_rps
        self.session = None
        self.visited_urls = set()
        self.root_url = root_url

        u = urlparse(root_url)
        self.main_netloc = u.netloc

        # requests datas
        self.time_deque = deque(maxlen=max_rps)

        # ElasticSearch values here
        self.es_session = None
        self.es_last_id = 0

        # Rabbit values here
        self.rabbit_connection = None
        self.rabbit_chanel = None
        self.rabbit_q = None
        self.rabbit_q_name = "urls_q"

    # TODO FIX
    async def check_rps_block(self):

        count = len(self.time_deque)

        if count < self.max_rps:
            self.time_deque.append(time.time_ns())

            return True

        now = time.time_ns()
        delta = self.time_deque[0] - now
        assert delta < 0
        if delta < NSEC_IN_SEC:
            if count == self.max_rps:
                self.time_deque.popleft()
            self.time_deque.append(now)

            return True
        else:
            False

        return True

        
    async def start_session(self):
        # bs4
        self.session = aiohttp.ClientSession()

        # es
        self.es_session = aiohttp.ClientSession()

        # rabbitmq
        self.rabbit_connection = await aio_pika.connect(
        "amqp://guest:guest@127.0.0.1/")
        self.rabbit_chanel = await self.rabbit_connection.channel()

        init_mongodb(dbname=DBNAME)

        self.rabbit_q = await self.rabbit_chanel.declare_queue(
             self.rabbit_q_name, auto_delete=True)

        await self.add_tasks([self.root_url])


    async def close_session(self):
        await self.session.close()
        await self.es_session.close()
        await self.rabbit_chanel.close()
        await self.rabbit_connection.close()


    def get_product(self, soup, product_url):
        def get_clear_price(price):
            num = []

            pattern = re.compile("^[0-9]+$")
            for s in price.split():
                if pattern.search(s):
                    num.append(s)

            res = "".join(num)
            return res

        prods = soup.find_all('span', 'name')
        if len(prods) != 1:
            return None

        item = prods[0]
        product_name = item.get_text()

        item = soup.find('span', 'add-discount-text-price')
        if item is None:
            return None
        price = int(get_clear_price(item.get_text()))
        
        item = soup.find('img', 'preview-photo')
        if item is None:
            return None
        img_url = item['src'][2:]
        

        discription = ''
        item = soup.find('div', 'description-text')
        if item is not None:
            discription = item.get_text()

        product = Product(product_name=product_name,
         discription=discription,
          price=price,
          img_url=img_url,
          product_url=product_url)
            
        return product

    def get_urls(self, soup):
        urls = set()
        
        for link in soup.find_all('a'):
            url = link.get('href')
            u = urlparse(url)
            if u.netloc == self.main_netloc and url not in self.visited_urls:
                urls.add(url)
                
        return urls

    async def add_tasks(self, urls):
        for url in urls:
            bdata = json.dumps({'url' : url})

            await self.rabbit_chanel.default_exchange.publish(
                aio_pika.Message(
                    body=bytes(bdata, 'utf-8'),
                    content_type="application/json"
               ),
                routing_key=self.rabbit_q_name
            )
    

    async def do_job(self, idx):
        # global COUNT 

        async for message in self.rabbit_q:
            async with message.process():
                data = json.loads(message.body)
                url = data['url']

                if url not in self.visited_urls:
                    self.visited_urls.add(url)

                    # COUNT -= 1
                    # if COUNT == 0:
                    #     return 

                    # soup = 0

                    while not await self.check_rps_block():
                        await asyncio.sleep()

                    async with self.session.get(url) as resp:
                        soup = BeautifulSoup(await resp.text(), 'html.parser')

                    new_urls = self.get_urls(soup)
                    await self.add_tasks(new_urls)


                    prod = self.get_product(soup, url)
                    if prod is not None:
                        await prod.save()
                        self.es_last_id += 1
                        print(prod)
                        await es_client.add_product(prod)

    async def crawl(self):
        await self.start_session()
        await asyncio.gather(*(self.do_job(i) for i in range(self.workers_count)))
        await self.close_session()
