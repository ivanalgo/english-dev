import scrapy
from scrapy.http import HtmlResponse
from scrapy import signals
import re
import os

class CommonSpider(scrapy.Spider):
    data_dir = "web_data/"
    access_url_set = set()
    start_url = ""

    def __init__(self, start_url):
        self.start_url = start_url

    def start_requests(self):
        start_urls = []

        for root, dirs, files in os.walk(self.data_dir):
            for file in files:
                # each spier just look for its own directory
                if not self.start_url in root:
                    continue

                if file == 'url':
                    url_path = os.path.join(root, file)
                    with open(url_path, 'r', encoding='utf-8') as f:
                        url = f.read()

                    if not os.path.exists(os.path.join(root, 'crwal')):
                        start_urls.append(url)
                    else:
                        access_url_set.add(url)

        if len(start_urls) == 0:
            start_urls = [self.start_url]

        for url in start_urls:
            print("url: ", url)
            yield scrapy.Request(url=url, callback=self.parse)

    def write_file(self, url, item, values):
        directory = "web_data/" + url
        if not os.path.exists(directory):
            os.makedirs(directory)

        path = os.path.join(directory, item)
        with open(path, 'w', encoding='utf-8') as f:
            for value in values:
                f.write(value + '\n')

    def extract_article(self, response):
        return (None, None)

    def write_article(self, url, tittle, content_blocks):
        self.write_file(url, 'url', [url])

        if tittle and content_blocks:
            # tittle
            self.write_file(url, 'tittle', [tittle])
            # content
            self.write_file(url, 'content', content_blocks)

    def parse_article(self, response):

        (tittle, content_texts) = self.extract_article(response)
        url = response.request.url
        if not tittle or not content_texts:
            return self.write_article(url, None, None)

        self.write_article(url, tittle, content_texts)

    def parse(self, response):
        url = response.request.url

        self.access_url_set.add(url)

        self.parse_article(response)

        relative_links = response.xpath('//a/@href').getall()
        absolute_links = [response.urljoin(link) for link in relative_links]

        for link in absolute_links:
            if not link.startswith("http"):
                continue
            # out of site
            if not link.startswith(self.start_url):
                continue

            # 跳过带锚点的 URL
            if "#" in link:
                continue

            if link in self.access_url_set:
                continue
            self.access_url_set.add(link)

            #print("hardy link: ", link)
            yield response.follow(link, callback = self.parse)

        self.write_file(url, 'crawl', ['yes'])
