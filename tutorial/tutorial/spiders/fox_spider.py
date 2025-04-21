 from .common_spider import CommonSpider

class FOXSpider(CommonSpider):
    name = "fox"

    def __init__(self):
        super().__init__("https://www.foxnews.com")
    
    # Override
    def extract_article(self, response):
        url = response.request.url

        title = response.xpath('//*[@id="wrapper"]/div[3]/div[2]/div/main/article/header/div[1]/h1/text()').get()
        if not title:
            return (None, None)

        all_texts = response.xpath(
	    '//*[@id="wrapper"]/div[3]/div[2]/div/main/article/div/div[1]/div//p//text()'
            ).getall()

        return (title, all_texts)
