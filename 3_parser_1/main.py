#!/usr/bin/env python3


from httpx import AsyncClient
from lxml import etree
from lxml.etree import HTMLParser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By


import asyncio
from progress.bar import IncrementalBar
from datetime import datetime
from time import sleep
import json
import re


URL = "http://dog-60.ru"


chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)


async def parseMainPage(url = URL) -> list:

    async with AsyncClient() as client:
        response = await client.get(url)

    if response.status_code == 200:
        html = etree.fromstring(response.text, HTMLParser())
        category_links = html.xpath('//ul[@class="clear"]//a/@href')
        return category_links
    
    else: 
        return 0
    

async def parseCategoryPage(url: str) -> list:

    async with AsyncClient() as client:
        response = await client.get(url)

    if response.status_code == 200:
        html = etree.fromstring(response.text, HTMLParser())
        products_links = html.xpath('//div[@class="items_photo"]/a/@href')
        return products_links
    
    else: 
        return 0


async def parseProductPage(url: str) -> dict:
    async with AsyncClient() as client:
        response = await client.get(url)
    
    if response.status_code == 200:
        dump = {}

        html = etree.fromstring(response.text, HTMLParser())

        dump["name"] = html.xpath('//div[@class="three_fifth first"]/h2/text()')[0]

        selector_values = html.xpath('//select[@id="select_ware_size"]/option/@value')

        if selector_values:
            price = []
            driver.get(url)

            for value in selector_values[1:]:
                select = Select(driver.find_element(By.ID,'select_ware_size'))
                select.select_by_value(value)
                sleep(1)
                price.append(driver.find_element(By.ID,'ware_price').text)

            dump['size - price'] = dict(zip(selector_values[1:], price))
        else:
            dump['price'] = html.xpath('//span[@id="ware_price"]/text()')
        
        dump['img_urls'] = html.xpath('//a[@class="fancybox"]/@href')
        dump['description'] = ''.join(html.xpath('//div[@class="wrapper row2"]/div[@id="container"]/div/p/text()'))
        dump['available'] = html.xpath('//div[@class="three_fifth first"]//span/text()')[0]
        return(dump)
    
    else:
        return 0
    

def MakeProductsDump(dump: list) -> None:
    date = str(datetime.now()).split(" ")[0]
    with open(f"results/{date}.json", "w", encoding="utf-8") as f:
        json.dump(dump, f, ensure_ascii=False, indent=2)

        
async def main():
    result = []
    category_links = await parseMainPage()

    if category_links:
        queue = []

        for category in category_links:
            products_links = await parseCategoryPage(category) 
            
            if products_links:
                for product_link in products_links:
                    queue.append(product_link)
            
            else:
                print(f"Ошибка парсинга страницы категории или страница пуста: {category}")

        bar = IncrementalBar('Товаров запаршено:', max = len(list(set(queue))))

        for link in list(set(queue)):
            bar.next()
            dump = await parseProductPage(link)
            if dump:
                result.append(dump)

            else:
                print(f"Ошибка парсинга категорий с страницы {link}") 
        
        bar.finish()
        MakeProductsDump(result)
    else:
        print(f"Ошибка парсинга категорий с главной страницы {URL}")

    driver.quit()

# async def test():
#     await parseProductPage("http://dog-60.ru/ware/vodilka-kapron-hrom")

if __name__ == "__main__":
    #asyncio.run(test())
    asyncio.run(main())