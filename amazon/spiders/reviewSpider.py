import scrapy
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider
from amazon.items import amazonProductReview
from amazon.utils  import get_asin_list


class reviewSpider(scrapy.Spider):
    name = 'review'
    

    def __init__(self, products=None, product=None,maxpages=None, *args, **kwargs):
        super(reviewSpider, self).__init__(*args, **kwargs)

        if product is not None:
            self.asinList = [product]
        elif products is not None:
            self.asinList = get_asin_list(products)
        else:
            CloseSpider("the arg product or products is important")

        if maxpages is not None: 
            self.maxpages = int(maxpages)
        else:
            self.maxpages = None

        
        

    def start_requests(self):
        # go to allReview function to parse the product page
        for asin in self.asinList:
            url = f"https://www.amazon.com/product-reviews/{asin}"
            yield scrapy.Request(url=url, callback=self.parse, meta={'asin': asin})
    

    def allReview(self, response):
        # get the link of all review page and follow it!!!
        allReviewPage = response.css("div#reviews-medley-footer a[data-hook='see-all-reviews-link-foot']::attr(href)").get()
        yield response.follow(url=allReviewPage, callback=self.parse)



    def parse(self, response):
        asin = response.meta.get('asin')
        for review in response.css("div#cm_cr-review_list div[data-hook='review']"):
            productReview = ItemLoader(item=amazonProductReview(), selector=review)
            productReview.add_value('asin',asin)
            productReview.add_css('title','a.review-title span::text')
            productReview.add_css('review','div.review-data span[data-hook="review-body"] span::text')
            productReview.add_css('reviewDate','span.review-date::text')
            productReview.add_css('reviewLoc','span.review-date::text')
            productReview.add_css('owner','span.a-profile-name::text')
            productReview.add_css('rating','i[data-hook="review-star-rating"] span::text')
            productReview.add_css('helpful','span[data-hook="helpful-vote-statement"]::text')

            yield productReview.load_item() 
        
        #next_page = response.css('div#cm_cr-pagination_bar li.a-last a::attr(href)').get()
        #if next_page is not None:
            #yield response.follow(next_page, callback=self.parse, meta={'asin': asin})

