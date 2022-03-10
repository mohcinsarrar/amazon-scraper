from pkg_resources import yield_lines
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.loader import ItemLoader
from amazon.items import amazonProduct



class AmazonSpider(scrapy.Spider):
    name = 'product'

    def __init__(self, category=None,maxpages=None, *args, **kwargs):
        super(AmazonSpider, self).__init__(*args, **kwargs)
        self.url = f'{category}'
        self.maxpages = int(maxpages)


    def start_requests(self):
        # callback getNbrPages function
        yield scrapy.Request(url=self.url, callback=self.getNbrPages)
        

    # get the number of page
    def getNbrPages(self, response):
        print('getNbrPages')
        nbrPages = response.css("div.s-pagination-container[role='navigation'] span span::text")[-1].get()
        for page in range(1,int(1)+1):
            next_url = f'{self.url}&page={page}'
            yield scrapy.Request(url=next_url, callback=self.parse_pages)


    # parse product link from each page
    def parse_pages(self, response):
        print('parse')
        for product in response.css("div[data-component-type='s-search-result']"):

            article_link = product.css('h2.a-size-mini a::attr(href)').get()

            # follow the product link
            if "/gp" not in article_link:
                yield response.follow(url=article_link, callback=self.parse_product)
               
    # parse product page
    def parse_product(self, response):
        print('parse_product')
        product = ItemLoader(item=amazonProduct(), selector=response)
        product.add_css('asin','input#ASIN::attr(value)')
        product.add_css('title','span#productTitle::text')
        product.add_css('brand','tr.po-brand td.a-span9 span::text')
        product.add_css('rating','div#averageCustomerReviews i.a-icon-star  span::text')
        product.add_css('price','div#corePrice_feature_div span.a-offscreen::text')
        product.add_css('picture','img#landingImage::attr(src)')
        # follow the article link and get respinse in the parse_article function
        yield product.load_item() 

