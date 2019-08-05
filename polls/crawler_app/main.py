import asyncio
import crawler
import time

from polls.models.db import init_mongodb, DBNAME

base_url = 'https://www.wildberries.ru/catalog/podarki/detyam?pagesize=100&sort=newly&bid=451b18d2-2621-4923-865b-c06df32eeb9b'
max_rps = 10
workers_count = 1

crawler_inst = crawler.Crawler(base_url, max_rps, workers_count)

start_time = time.time()

loop = asyncio.get_event_loop()
loop.run_until_complete(crawler_inst.crawl())