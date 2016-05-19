# -*- coding: utf-8 -*-
import scrapy
import logging

from scrapy.http import FormRequest

class PttSpider(scrapy.Spider):
    name = "jp_travel"
    allowed_domains = ["ptt.cc"]
    start_urls = (
        'https://www.ptt.cc/bbs/Japan_Travel/index.html',
        'https://www.ptt.cc/bbs/Gossiping/index.html'
    )

    _retries = 0
    MAX_RETRY = 1

    def parse(self, response):
        if len(response.xpath('//div[@class="over18-notice"]')) > 0:
            if self._retries < PttSpider.MAX_RETRY:
                self._retries += 1
                logging.warning('retry {} times...'.format(self._retries))
                return FormRequest.from_response(response,
                                                formdata={'yes': 'yes'},
                                                callback=self.parse)
            else:
                logging.warning('you cannot pass')

        else:
            filename = response.url.split('/')[-2] + '.html'
            with open(filename, 'wb') as f:
                f.write(response.body)
