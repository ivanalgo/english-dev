from .common_spider import CommonSpider

class WIKISpider(CommonSpider):
    name = "wiki"

    def __init__(self):
        super().__init__("https://en.wikipedia.org")
    
    # Override
    def extract_article(self, response):
        url = response.request.url

        if not url.startswith("https://en.wikipedia.org/wiki/"):
            return (None, None)

        suffix = url[len("https://en.wikipedia.org/wiki/"):]
        if ":" in suffix:
    	    return (None, None)

        title = response.xpath('/html/head/title/text()').get()
        # Remove the tailing part
        title = title.replace(" - Wikipedia", "")

        paragraphs = response.xpath('//*[@id="mw-content-text"]//p//text()').getall()
        return (title, paragraphs)
