import asyncio
import crawler

base_url = 'https://www.wildberries.ru/catalog/zhenshchinam/bele-i-kupalniki/trusy'
max_rps = 10
workers_count = 1

crawler_inst = crawler.Crawler(base_url, max_rps, workers_count)

loop = asyncio.get_event_loop()
loop.run_until_complete(crawler_inst.crawl())