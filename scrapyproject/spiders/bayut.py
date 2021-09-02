from typing import Sized
import scrapy

class bayut(scrapy.Spider):
    name = 'bayutscrap'
    start_urls = ['https://www.bayut.com/to-rent/property/dubai/']

    def parse(self, response):
        for products in response.css('article.ca2f5674'):
            
            inside_item = products.css('a._287661cb').attrib['href']
            if inside_item is not None:

                yield response.follow(inside_item, callback = self.parse_item)



        next_page = response.css('a.b7880daf::attr(href)').getall()[-1] 
        if next_page is not None:

            yield response.follow(next_page,callback=self.parse)    

    def parse_item(self,response):
        for items in response.css('div.a808fc60'):
            yield {
                "property_id" : items.css('span._812aa185::text').getall()[2],
                "purpose" : items.css('span._812aa185::text').getall()[1],
                'Type' : items.css('span._812aa185::text').get(),
                "added_on" : items.css('span._812aa185::text').getall()[-1],
                "furnishing" : items.css('span._812aa185::text').getall()[3],
                "price" : {
                     "currency": items.css('span.e63a6bfb::text').get(),
                     "amount": items.css('span._105b8a67::text').get(),
                },
                "location" : items.css('div._1f0f1758::text').get(),
               "bed_bath_size" : {
                   "bedrooms": items.css('span.fc2d1086::text').getall()[0].replace('Beds','').replace('Bed','').replace('Studio',"0").strip(),
                   "bathrooms": items.css('span.fc2d1086::text').getall()[1].replace('Baths','').replace('Bath','').strip(),
                   "Size" : items.css('span.fc2d1086 span::text').get(),
               },
    
                "permit_number": items.css('span.ff863316::text').getall()[-1],
                "agent_name": items.css('span._55e4cba0::text').get(),
                "image_url": items.css('img.bea951ad::attr(src)').get(),
                "breadcrumbs" : items.css('span._812aa185::text').get() + 's ' + items.css('span._812aa185::text').getall()[1] + ' in ' + ' > '.join(items.css('div._1f0f1758::text').get().split(', ')[::-1]),
                "amenities" :  items.css('span._005a682a::text').getall(),
                "description" : ' '.join(items.css('span._2a806e1e::text').getall()),
            
            }