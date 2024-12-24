import sys
sys.path.append("/Users/hardy/english-dev/tutorial/tutorial/spiders")
from common_spider import CommonSpider


class APSpider(CommonSpider):
    name = "ap"

    def __init__(self):
        super().__init__("https://apnews.com/") 

    # Override
    def extract_article(self, response):
        url = response.request.url
        tittle = response.xpath('.//div[@class="Page-content"]//h1[@class="Page-headline"]/text()').get()
        content_blocks = response.xpath('.//div[@class="Page-content"]//div[@class="RichTextStoryBody RichTextBody"]')
        content_texts = []

        for block in content_blocks:
                # 获取每个内容块的文本内容
                text = block.xpath('.//p//text()').getall()
                content_texts += text

        return (tittle, content_texts)
