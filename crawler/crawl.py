import hashlib

import scrapy

from crawler.contract_parser import parse_price, parse_date, parse_contract_party, parse_string
from crawler.helpers import hash_url, remove_url_trailing_slash, generate_start_urls

NEXT_PAGE_SELECTOR = '.pagination-next'
CONTRACT_DETAIL_SELECTOR = 'td > a'

CONTRACT_DETAIL = {
    'type_selector': 'table th:contains("Typ") + td',
    'number_selector': 'table th:contains("Č. zmluvy") + td',
    'resort_selector': 'table th:contains("Rezort") + td',
    'customer_selector': 'table th:contains("Objednávateľ") + td',
    'supplier_selector': 'table th:contains("Dodávateľ") + td',
    #'supplier_id_selector': 'table th:contains("Dodávateľ") + td',
    'name_selector': 'table th:contains("Názov zmluvy") + td strong',
    'id_selector': 'table th:contains("ID zmluvy") + td strong',
    'note_selector': 'table th:contains("Poznámka") + td',
    'final_price_eur_selector': 'div.area.area4 > div.last > span',
    'publication_date_selector': 'table th:contains("Dátum zverejnenia") + td',
    'conclusion_date_selector': 'table th:contains("Dátum uzavretia") + td',
    'effective_date_selector': 'table th:contains("Dátum účinnosti") + td',
    'expiration_date_selector': 'table th:contains("Dátum platnosti do") + td',
}


class ContractSpider(scrapy.Spider):
    name = 'crzp'

    start_urls = generate_start_urls()

    custom_settings = {
        'CONCURRENT_REQUESTS': 3,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en',
            'Author': 'xhoffer@stuba.sk',
            'Purpose': 'FIIT STU Bratislava, project for academic purposes',
        },
        # Wait N seconds before each request to respect rate limits
        'DOWNLOAD_DELAY': 1.5,

        # Use BFS instead of default DFS
        'DEPTH_PRIORITY': 1,
        'SCHEDULER_DISK_QUEUE': 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue',

        # Pipelines for processing crawled items
        'ITEM_PIPELINES': {
            'crawler.visited_url_pipeline.VisitedUrlPipeline': 100
        },
        'LOG_LEVEL': 'INFO'
    }

    def __init__(self):
        self.visited = {}  # MD5 hashes of already visited URLs

    def parse(self, response):

        contract_details_links = response.css(CONTRACT_DETAIL_SELECTOR)
        unvisited = []
        for cd in contract_details_links:
            url_to_follow = 'https://www.crz.gov.sk' + cd.attrib['href']
            if hash_url(url_to_follow) in self.visited:
                print("URL already visited before, skipping: ", url_to_follow)
                continue
            unvisited.append(cd)

        yield from response.follow_all(unvisited, self.parse_contract)

        next_page_link = response.css(NEXT_PAGE_SELECTOR)
        yield from response.follow_all(next_page_link, self.parse)

    def parse_contract(self, response):
        def extract_with_css(query: str):
            return response.css(query).get()

        supplier_name, supplier_address = parse_contract_party(
            response.css(CONTRACT_DETAIL['supplier_selector'] + '::text').getall())
        customer_name, customer_address = parse_contract_party(
            response.css(CONTRACT_DETAIL['customer_selector'] + '::text').getall())

        if response.status == 200:
            yield {
                'url': response.url,
                'id': parse_string(extract_with_css(CONTRACT_DETAIL['id_selector'] + '::text')),
                'type': parse_string(extract_with_css(CONTRACT_DETAIL['type_selector'] + '::text')),
                'number': parse_string(extract_with_css(CONTRACT_DETAIL['number_selector'] + '::text')),
                'resort': parse_string(extract_with_css(CONTRACT_DETAIL['resort_selector'] + '::text')),
                'customer': customer_name,
                'customer_address': customer_address,
                'supplier': supplier_name,
                'supplier_address': supplier_address,
                #'contract_supplier_id': parse_string(
                #    extract_with_css(CONTRACT_DETAIL['supplier_id_selector'] + '::text')),
                'name': parse_string(extract_with_css(CONTRACT_DETAIL['name_selector'] + '::text')),
                'note': parse_string(extract_with_css(CONTRACT_DETAIL['note_selector'] + '::text')),
                'final_price_eur': parse_price(
                    extract_with_css(CONTRACT_DETAIL['final_price_eur_selector'] + '::text')),
                'publication_date': parse_date(
                    extract_with_css(CONTRACT_DETAIL['publication_date_selector'] + '::text')),
                'conclusion_date': parse_date(
                    extract_with_css(CONTRACT_DETAIL['conclusion_date_selector'] + '::text')),
                'effective_date': parse_date(
                    extract_with_css(CONTRACT_DETAIL['effective_date_selector'] + '::text')),
                'expiration_date': parse_date(
                    extract_with_css(CONTRACT_DETAIL['expiration_date_selector'] + '::text')),
            }
