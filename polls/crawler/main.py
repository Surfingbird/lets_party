import asyncio
import crawler

base_url = 'https://www.wildberries.ru/catalog/8454974/detail.aspx?targetUrl=GP'
max_rps = 10
workers_count = 1

crawler_inst = crawler.Crawler(base_url, max_rps, workers_count)

loop = asyncio.get_event_loop()
loop.run_until_complete(crawler_inst.crawl())