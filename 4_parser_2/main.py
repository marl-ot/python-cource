from httpx import AsyncClient
from lxml import etree
from lxml.etree import HTMLParser


import os
import gc
import asyncio
from typing import Union
import json
from datetime import datetime
import time

start = time.time()

MAIN_URL = "https://amazin.su"
URL = "https://amazin.su/shop/zotovary"


async def getLinksFromMainPage(url=URL) -> Union[list, int]:
    """Данная функция находит ссылки на все страницы"""

    async with AsyncClient() as client:
        response = await client.get(url)

    if response.status_code == 200:
        tree = etree.fromstring(response.text, HTMLParser())
        pages_counter = int(tree.xpath(
            '//span[@class="plist"]/a/@href')[-1].split(";")[-1])
        return [url] + [url+f';{index}' for index in range(2, pages_counter+1)]

    return 0


async def getProductsLinks(url: str) -> Union[list, int]:
    """Данная функция находит ссылки на все товары"""
    async with AsyncClient() as client:
        response = await client.get(url)

    if response.status_code == 200:
        tree = etree.fromstring(response.text, HTMLParser())
        links = tree.xpath('//a[@class="shop-item-title"]/@href')
        return [MAIN_URL + link for link in links]

    return 0


async def parseProduct(url: str) -> Union[list, int]:
    """Данная функция собирает информацию о продукте"""

    async with AsyncClient() as client:
        response = await client.get(url)

    if response.status_code == 200:
        dump = {}

        # Парсинг каталога товаров в категории зоотовары.
        # По каждому название*, идентификатор*, артикул*, весовая* и ценовая сетка* (с учётом скидки),
        # производитель*, картинки*, гарантия*, единицы*,
        # вес*, описание*, инструкции*, характеристики*, наличие*, вложенность категорий*, отзывы* (при наличии).

        tree = etree.fromstring(response.text, HTMLParser())
        dump["название"] = tree.xpath('//h1[@class="eTitle"]/text()')[0]
        dump["идентификатор"] = int(url.split('/')[-3])
        dump["цена"] = tree.xpath('//span[@class="newprice"]/span/text()')[0]
        dump["вложенность категорий"] = '/'.join(tree.xpath(
            '//span[@itemprop="itemListElement"]/a/span/text()'))

        options_name = tree.xpath(
            '//div[@class="col-9"]/ul[@class="shop-options"]/li/span[@class="opt"]/text()')
        options_name = [name for name in options_name if name not in [
            ":", 'Артикул', 'Наличие', 'Теги:']]

        options_data = tree.xpath(
            '//ul[@class="shop-options"]/li/span[@class="val"]/text()')

        for i in range(len(options_name)):
            dump[options_name[i]] = options_data[i]

        dump["Артикул"] = tree.xpath(
            '//ul[@class="shop-options"]/li/span[@class="val art"]/text()')[0]
        dump["Наличие"] = tree.xpath(
            '//ul[@class="shop-options"]/li/span[@class="val stock"]/text()')[0]

        dump["описание"] = '\n'.join(tree.xpath(
            '//div[@itemprop="description"]/text()') + tree.xpath('//div[@id="DESCRIPTION"]//text()'))

        async with AsyncClient() as client:
            response = await client.get(url+"#DOCS")
            if response.status_code == 200:
                tree = etree.fromstring(response.text, HTMLParser())
                dump["инструкции"] = "\n".join(
                    tree.xpath('//table[@class="docs"]//text()'))

        async with AsyncClient() as client:
            response = await client.get(url+"#COM")
            if response.status_code == 200:
                tree = etree.fromstring(response.text, HTMLParser())
                desc = tree.xpath(
                    '//div[@class="uc-message cMessage"]/text()')
                if desc:
                    dump["отзывы"] = desc

        img_urls = tree.xpath('//img[@class="gphoto"]/@src')
        dump["картинки"] = [MAIN_URL + url for url in img_urls]
        return dump

    return 0


def MakeProductsDump(dump: list) -> None:

    date = str(datetime.now()).split(" ")[0]
    with open(f"result/{date}.json", "w", encoding="utf-8") as f:
        json.dump(dump, f, ensure_ascii=False, indent=2)

    print(f"Данные записаны в result/{date}.json")


async def main() -> None:
    products_links = []

    pages_links = await getLinksFromMainPage(URL)

    if pages_links:
        for page_link in pages_links:
            products = await getProductsLinks(page_link)
            if products:
                for product in products:
                    products_links.append(product)
            else:
                print(f"Не удалось запарсить {page_link}")

        result = []
        for link in products_links:
            data = await parseProduct(link)
            # print(json.dumps(data, ensure_ascii=False, indent=3))
            if data:
                result.append(data)
            else:
                print(f"Не удалось запарсить {link}")

        MakeProductsDump(result)
    else:
        print(f"Не удалось запарсить {URL}")

    gc.collect()



if __name__ == "__main__":
    while True:
        asyncio.run(main())

        # time.sleep(5 * 24 * 60 * 60)

end = time.time() - start
print(end)