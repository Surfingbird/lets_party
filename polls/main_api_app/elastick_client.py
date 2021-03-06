import aiohttp
import asyncio
import json

from polls.models.fake_model_manager import FakeModelManager

class ElastickClient:
    def __init__(self, loop=None, path='http://0.0.0.0:9200/products/product/'):
        self.session = None
        self.last_insert_id = 100
        self.loop = loop
        self.path = path

    def connect(self):
          self.session = aiohttp.ClientSession(loop=self.loop)

    async def disconnect(self):
        await self.session.close()

    async def add_product(self, product):
        data =  product.__dict__.copy()
        _id = data.pop('_id')
        data.pop('changed')
        data['id'] = _id

        self.last_insert_id += 1
        url = self.path + str(self.last_insert_id) + '?pretty'

        async with self.session.put(url, json=(data)) as resp:
            pass 

    async def get_products(self, pattern):
        query = {"query": { "match": { "product_name": pattern } }}

        url = self.path + '_search'
        result = []

        async with self.session.get(url, json=(query)) as resp:
            data = await resp.json()

            for node in data['hits']['hits']:
                lite_info = dict()

                product = node['_source']
                lite_info['_id'] = product['id']
                lite_info['product_name'] = product['product_name']

                result.append(lite_info)

        return result


    async def get_products_full(self, pattern):
        query = {"query": { "match": { "product_name": pattern } }}

        url = self.path + '_search'
        result = []

        async with self.session.get(url, json=(query)) as resp:
            data = await resp.json()

            for node in data['hits']['hits']:
                product = node['_source']
                _id = product.pop('id')
                product['_id'] = _id

                result.append(product)

        return result