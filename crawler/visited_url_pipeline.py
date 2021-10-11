import hashlib

from crawler.helpers import hash_url

VISITED_URLS_FILE = 'visited.txt'


class VisitedUrlPipeline:

    def __init__(self):
        self.spider = None

    def open_spider(self, spider):
        self.spider = spider
        self._load_visited_urls()

    def close_spider(self, spider):
        self._write_visited_urls()

    def process_item(self, item, spider):
        self._mark_url_as_visited(item['url'])
        return item

    def _load_visited_urls(self):
        with open(VISITED_URLS_FILE, 'r+') as f:
            print("Loading visited URLs from previous runs...")
            lines = f.read().splitlines()
            for line in lines:
                self.spider.visited[line] = True
            print('Loaded', len(lines), ' previously visited URLs')

    def _mark_url_as_visited(self, url: str):
        url_hash = hash_url(url)
        self.spider.visited[url_hash] = True

    def _write_visited_urls(self):
        with open(VISITED_URLS_FILE, 'w+') as f:
            for url in self.spider.visited.keys():
                f.write(url + '\n')
