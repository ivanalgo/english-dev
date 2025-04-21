from .common_spider import CommonSpider

class BBCSpider(CommonSpider):
    name = "bbc"

    def __init__(self):
        super().__init__("https://www.bbc.com")
    
    # Override
    def extract_article(self, response):
        url = response.request.url
        article_elem = response.xpath('//*[@id="main-content"]/article')

        if article_elem:
            tittle = article_elem.xpath('.//div[@data-component="headline-block"]/h1/text()').get()
            content_blocks = article_elem.xpath('.//div[@data-component="text-block"]')

        if not article_elem or not tittle or not content_blocks:
            return (None, None)

        # 查找所有的内容块
        content_blocks = article_elem.xpath('.//div[@data-component="text-block"]')
        content_texts = []
        for block in content_blocks:
                # 获取每个内容块的文本内容
                text = block.xpath('.//p//text()').getall()
                # 每个p下面有html内容修饰时，都会引入很多html标记，在这种情况下，
                # 会隔断当前的文本分析，把后面内容变成列表下一个元素
                # 为了还原当前段落，我们把text列表合并成一段文字
                paragraph = ""
                for item in text:
                    paragraph += item

                content_texts.append(paragraph) 

        return (tittle, content_texts)
