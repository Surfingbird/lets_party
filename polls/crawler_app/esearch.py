import asyncio
import aiohttp
import aio_pika
import json

from bs4 import BeautifulSoup
from urllib.parse import urlparse
import random

from faker import Faker
fake = Faker()

import re

import polls.models.model_manager as model_manager
import polls.models.fake_model_manager as fake_model_manager

mm = model_manager.ModelManager()
fm = fake_model_manager.FakeModelManager()

scheme = "http://"
es_index = 'products'
es_type = 'product'
es_url = '127.0.0.1:9200'

main_url = scheme + es_url + "/" + es_index + "/" + es_type + "/"

async def add_product_in_app():
     product = model_manager.Product(fake.name(), fake.text(), random.uniform(1, 1000), fake.url(), fake.url())

     pid = await mm.create_product(product)
     _id = str(pid)

     d = product.to_dict()
     d['p_id'] = _id

     url = main_url + "1" + "?pretty"

     async with aiohttp.ClientSession() as session:
         async with session.put(url, json=(d)) as resp:
             print(await resp.text())


async def match_pattern(pattern):
    query = {''
        '_source' : True,
        'query' : {
            'match' : {
                'content' : 'Трусы'
            }
        }
    }

    url = main_url + "_search&pretty"

    async with aiohttp.ClientSession() as session:
         async with session.get(url, json=(query)) as resp:
             print(await resp.text())




    
loop = asyncio.get_event_loop()
loop.run_until_complete(add_product_in_app())
loop.run_until_complete( match_pattern(""))





