# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from unicodedata import category
import scrapy
from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags
from itemloaders.processors import TakeFirst, MapCompose
from amazon.utils  import *


class amazonProduct(Item):
    asin = Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    title = Field(input_processor = MapCompose(remove_tags,parse_title), output_processor = TakeFirst())
    brand = Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    rating = Field(input_processor = MapCompose(remove_tags,parse_rating), output_processor = TakeFirst())
    price = Field(input_processor = MapCompose(remove_tags,parse_price), output_processor = TakeFirst())
    picture = Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())

class amazonProductReview(Item):
    asin = Field()
    title = Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    review = Field(input_processor = MapCompose(remove_tags,parse_review_text), output_processor = TakeFirst())
    reviewDate = Field(input_processor = MapCompose(remove_tags,parse_date), output_processor = TakeFirst())
    reviewLoc = Field(input_processor = MapCompose(remove_tags,parse_loc), output_processor = TakeFirst())
    owner = Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    rating = Field(input_processor = MapCompose(remove_tags,parse_rating), output_processor = TakeFirst())
    helpful = Field(input_processor = MapCompose(remove_tags,parse_helpful), output_processor = TakeFirst())
    sentiment = Field()



class AmazonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
