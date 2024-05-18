import re
import scrapy
from typing import Any
from scrapy.http import Response
from yelpCrawler.items import YelpcrawlerItem


class YelpSpider(scrapy.Spider):
    name='yelp'
    allowed_domains=['www.yelp.com.br', 'yelp.com.br']
    start_urls = ['https://www.yelp.com.br/s%C3%A3o-paulo']

    def parse(self, response: Response) -> Any:
        for page in response.xpath('/html/body/yelp-react-root/div[1]/div[2]/div[1]/div/header/div/div[2]/div/nav/div[1]//a/@href'):
            yield response.follow(page, self.menu_items)

    def menu_items(self, response: Response):
        item = YelpcrawlerItem()
        item['category'] = response.xpath('//*[@id="search_description"]/@value').get()
        item['page'] = response.xpath('//div[contains(@class,"pagination-link-current")]//text()').get()

        for content in response.xpath('//div[contains(@class,"businessName")]//h3'):
            rank = content.xpath('text()').get()
            content_url = content.xpath('a/@href').get()
            yield response.follow(content_url, self.content ,cb_kwargs={"item": item, "rank": rank})

        next_pg = response.xpath('//div[contains(@class,"pagination-links")]//@href')
        if next_pg:
            for pg in next_pg:
                yield response.follow(pg, self.menu_items)

    def content(self, response: Response, item, rank):

        item['rank'] = rank
        item['image'] = response.xpath('/html/body/yelp-react-root/div[1]/div[4]//img/@src').getall()
        item['priceRange'] = response.xpath('/html/body/yelp-react-root/div[1]/div[4]/div[1]/div[1]/div/div/span[2]/span/text()').get()
        item['attributes'] = response.xpath('//*[@id="main-content"]/section//span//text()').getall()
        item['link'] = response.urljoin(response.xpath('//*[@id="main-content"]/div/ul//a/@href').get())
        item['hours'] = response.xpath('//*[@id="location-and-hours"]/section//table//text()').getall()
        item['reviews'] = response.xpath('/html/body/yelp-react-root/div[1]/div[4]/div[1]/div[1]/div/div/div[2]/div[2]//a/text()').get()
        item['score'] =  response.xpath('/html/body/yelp-react-root/div[1]/div[4]/div[1]/div[1]/div/div/div[2]/div[2]//span/text()').get()

        title = response.xpath('//div[contains(@class,"photo-header-content")]//h1/text()').get()
        if title:
            item['title'] = title
        else:
            title_02 = response.xpath('//*[@id="main-content"]//h1/text()').get()
            item['title'] = title_02

        address = response.xpath('//*[@id="main-content"]//section//address//text()').getall()
        if address:
            item['address'] = ' '.join(address)
        else:
            address_02 =  response.xpath('//*[@id="location-and-hours"]//section/div[2]/div[1]//text()').getall()
            item['address'] = ' '.join(address_02)

        infos_list = response.xpath('/html/body/yelp-react-root/div[1]/div[6]/div/div[1]/div[2]/aside/section//text()').getall()
        if infos_list:
            for i in range(0,len(infos_list),2):
                if 'telefone' in infos_list[i]:
                    item['phone'] = infos_list[i+1].strip()
                elif 'Website' in infos_list[i]:
                    item['website'] = infos_list[i+1].strip()
                else:
                    break
        else:
            infos_list_02 = response.xpath('/html/body/yelp-react-root/div[1]/div[5]/div/div[1]/div[2]/aside/section[1]//text()').getall()
            if infos_list_02:
                for i in range(0,len(infos_list_02),2):
                    if 'telefone' in infos_list_02[i]:
                        item['phone'] = infos_list_02[i+1].strip()
                    elif 'Website' in infos_list_02[i]:
                        item['website'] = infos_list_02[i+1].strip()
                    else:
                        break

        yield item




