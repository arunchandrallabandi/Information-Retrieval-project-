import scrapy
from urllib.parse import urljoin
import os

PAGES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "pages")
os.makedirs(PAGES_DIR, exist_ok=True)

MAX_PAGES = 30

class DocumentSpider(scrapy.Spider):
    name = "document_spider"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/Information_retrieval"]

    custom_settings = {
        'DEPTH_LIMIT': 2,
        'DOWNLOAD_DELAY': 0.3,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 0.3,
        'AUTOTHROTTLE_MAX_DELAY': 1.0,
    }

    page_count = 0
    visited_urls = set()

    def parse(self, response):
        if self.page_count >= MAX_PAGES:
            return

        filename = f"page_{self.page_count + 1}.html"
        path = os.path.join(PAGES_DIR, filename)
        with open(path, "wb") as f:
            f.write(response.body)

        self.page_count += 1
        self.visited_urls.add(response.url)
        self.logger.info(f"Saved {filename}: {response.url}")

        links = response.css('a::attr(href)').getall()
        for link in links:
            absolute_url = urljoin(response.url, link)
            if absolute_url not in self.visited_urls and absolute_url.startswith("https://en.wikipedia.org/wiki/"):
                yield scrapy.Request(absolute_url, callback=self.parse)
