import asyncio
import  aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

from polls.models import product

prod_manager = product.ProductManager()

class WrappedUrlQueue:
    def __init__(self, max_rps):
        self.q = asyncio.Queue()
        self.max_rps = max_rps

    def put_nowait(self, url):
        self.q.put_nowait(url)

    async def put(self, url):
        await self.q.put(url)

    async def put_many(self, urls):
        for url in urls:
            await self.put(url)
    
    async def get(self):
        return await self.q.get()

        
class Crawler:
    def __init__(self, root_url, max_rps, workers_count):
        self.workers_count = workers_count
        self.max_rps = max_rps
        self.q = WrappedUrlQueue(max_rps)
        self.session = None
        self.visited_urls = set()

        u = urlparse(root_url)
        self.main_netloc = u.netloc

        self.q.put_nowait(root_url)

    async def start_session(self):
        self.session = aiohttp.ClientSession()

    async def close_session(self):
        await self.session.close()

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
        price = get_clear_price(item.get_text())
        
        item = soup.find('img', 'preview-photo')
        if item is None:
            return None
        img_url = item['src'][2:]
        

        discription = ''
        item = soup.find('div', 'description-text')
        if item is not None:
            discription = item.get_text()
            
        return product.Product(product_name, discription, price, img_url, product_url)

    def get_urls(self, soup):
        urls = set()
        
        for link in soup.find_all('a'):
            url = link.get('href')
            u = urlparse(url)
            if u.netloc == self.main_netloc and url not in self.visited_urls:
                urls.add(url)
                
        return urls
    
    # TODO сделать бесконечным циклом
    async def do_work(self, idx):
        for i in range(10):
            url = await self.q.get()
            if url not in self.visited_urls:
                self.visited_urls.add(url)

                soup = ''
                async with self.session.get(url) as resp:
                    soup = BeautifulSoup(await resp.text(), 'html.parser')

                new_urls = self.get_urls(soup)
                await self.q.put_many(new_urls)

                prod = self.get_product(soup, url)
                if prod is not None:
                    print(prod)
                    await prod_manager.create_product(prod)

    async def crawl(self):
        await self.start_session()
        await asyncio.gather(*(self.do_work(i) for i in range(self.workers_count)))
        await self.close_session()
