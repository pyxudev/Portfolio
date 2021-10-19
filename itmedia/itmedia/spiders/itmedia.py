import scrapy
import re
import subprocess
from ..items import ItmediaItem

class ItemediaSpider(scrapy.Spider):
    name = 'itmedia'

    def start_requests(self):
        url = 'https://www.itmedia.co.jp/business/'
        yield scrapy.Request(url=url, callback=self.parse_list)
    
    def parse_list(self, response):
        news_list = response.css('#colBoxNewNews > div.colBoxInner > div')
        for news in news_list:
            script_title = news.css('div.colBoxTitle > h3 > a > script').get()
            title = script_title.replace("<script>cutTitle('", "").replace("','nne');</script>", "")
            link = 'https:' + news.css('div.colBoxTitle > h3 > a').attrib['href']

            item = ItmediaItem()
            item['title'] = title
            item['link'] = link
            yield item