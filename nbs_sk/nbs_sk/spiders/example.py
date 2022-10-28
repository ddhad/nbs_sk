import io
import json
import re

import PyPDF2
import scrapy

from ..items import NbsSkItem
from datetime import datetime


class ExampleSpider(scrapy.Spider):
    name = 'example'

    def start_requests(self):
        url = 'https://nbs.sk/wp-json/nbs/v1/post/list?_locale=user'
        offset = 0
        limit = 20
        headers = {
            "Accept": "application/json, */*;q=0.1",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Cookie": "pll_language=en",
        }
        for i in range(2):
            payload = {
                "gbConfig": {
                    "limit": 5,
                    "categories": [32424, 32416, 8, 32418, 32420],
                    "className": "",
                    "template": "links",
                    "tags": []
                },
                "lang": "en",
                "limit": limit,
                "offset": offset,
                "filter": {"lang": "en"},
                "onlyData": False
            }
            yield scrapy.Request(url=url, method="POST", body=json.dumps(payload),
                                 headers=headers, callback=self.parse)
            offset += 20

    def parse(self, response):
        data = json.loads(response.body)
        articles = re.findall(r'(?<=<a)(?:.|\s)*?(?=<\/a)', data['html'])
        for article in articles:
            item = NbsSkItem()
            item['title'] = re.findall(r'(?<=h3".).*(?=</h2)', article)[0]
            date = re.findall(r'(?<=date".).*(?=</div)', article)[0]
            item['date'] = datetime.strptime(date, "%d. %m. %Y").strftime("%Y-%m-%d")
            item['url'] = re.findall(r'(?<=href=").*(?="  )', article)[0]
            labels = re.findall(r'(?<=>).*(?=</div)', article)
            del labels[-1]
            item['labels'] = labels
            yield scrapy.Request(url=item['url'], callback=self.parse_article,
                                 dont_filter=True, cb_kwargs=dict(item=item))

    def parse_article(self, response, item):
        if '/dokument/' in response.request.url or '/pdf/' in response.request.url:
            reader = PyPDF2.PdfFileReader(io.BytesIO(response.body), strict=False)
            content = ''
            for page in reader.pages:
                content += page.extractText()
            item['content'] = content
            urls = re.findall(r'https:.*?(?=\s|>|\)|"|\')', content)
        else:
            content = response.xpath("//div[@class='nbs-content'] | //article[@class='nbs-post'] | "
                                     "(//div[@class='section'])[position() > 1]").get()

            urls = re.findall(r'https:.*?(?=\s|>|\)|"|\')', content)
            clean = re.compile(r'<(?!\/?(?=>|\s.*>))\/?.*?>')
            content = re.sub(clean, ' ', content)
            item['content'] = " ".join(content.split())
        if urls:
            item['urls'] = urls
        else:
            item['urls'] = []

        yield item
