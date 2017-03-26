# coding:utf-8
import scrapy
import os
import re
from selenium import webdriver
from scrapy import Selector


class QuotesSpider(scrapy.Spider):
    name = "yzdata"
    start_urls = ['https://db.yaozh.com/yaopinzhongbiao?name={0}&zb_shengchanqiye={1}&first={2}&pageSize=20&p={3}',]
    first = '全部'
    p = '1'
    # webdriver = web_driver = webdriver.Chrome("/Users/chc/Desktop/python/kaggle/webdriver/chromedriver")

    data = [
        {"com": "恒瑞医药", "pro": "多西他赛"},# 170条
        # {"com": "恒瑞医药", "pro": "奥沙利铂"},# 194条
        # {"com": "恒瑞医药", "pro": "厄贝沙坦"},# 104条

    ]

    def start_requests(self):
        cookies = {
            'PHPSESSID': '169t3qjps2uadhdlu7q6nrl020',
            'MEIQIA_EXTRA_TRACK_ID': '0070956c107b11e7a7c00246fd076266',
            'WAF_SESSION_ID': '7c11911792738023131881d90b524638',
            # 'WAF_SESSION_ID': 'f2e50c98c8ba11854406efcb42a09786',
            'mylogin': '1',
            'UtzD_f52b_saltkey':'oWr2AyrG',
            'UtzD_f52b_lastvisit':'1490347056',
            'UtzD_f52b_ulastactivity': '1489737935%7C0',
            'UtzD_f52b_creditnotice': '0D0D2D0D0D0D0D0D0D371681',
            'UtzD_f52b_creditbase': '0D0D431D0D0D0D0D0D0',
            'UtzD_f52b_creditrule': '%E6%AF%8F%E5%A4%A9%E7%99%BB%E5%BD%95',
            '_gat': '1',
            'think_language': 'zh-CN',
            'yaozh_logintime': '1490502368',
            'yaozh_user': '385042%09gjpharm',
            'yaozh_userId': '385042',
            'db_w_auth': '371681%09gjpharm',
            'UtzD_f52b_lastact': '1490502368%09uc.php%09',
            'UtzD_f52b_auth': 'e3d5gRSSV6rZBMDIXFGsojHL15i63tnOIxQdiekgVIJGtv9id%2F7tU98TZ5wtYWhumDVOv6DpAXI5yCzYTZ8zkoNetx0',
            '_ga': 'GA1.2.714695514.1490350613',
            'Hm_lvt_65968db3ac154c3089d7f9a4cbb98c94': '1490350613',
            'Hm_lpvt_65968db3ac154c3089d7f9a4cbb98c94': '1490502403',
            'zbpreid': ''
        }

        for d in self.data:
            zb_shengchanqiye = d["com"]
            yname = d["pro"]
            url = self.start_urls[0].format(yname, zb_shengchanqiye, self.first, self.p)
            # print(url)
            # self.yname = yname
            # self.zb_shengchanqiye = zb_shengchanqiye
            yield scrapy.Request(url=url, callback=self.parse, cookies=cookies)

    def parse(self, response):
        filename = 'test.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Save file %s' % filename)
        try:

            total = response.xpath('//div[@class="tr offset-top"]/@data-total').extract_first()
            print(total)
            page = int(int(total) / 20) + 1
        except TypeError:
            print("no page")
            print(response.url)
            # return

        # selector = Selector(text=self.webdriver.page_source)
        # next_page = selector.xpath('//div[@class="tr offset-top pagination"]/a/@href').extract()
        # print(next_page)
        # next_page_num = next_page[len(next_page) - 1]
        # print(next_page_num)

        for tr in response.xpath('//tbody/tr'):
            yield{
                'general_name': tr.xpath('td[2]/span/text()').extract_first(),
                'name': tr.xpath('td[3]/text()').extract_first(),
                'type': tr.xpath('td[4]/text()').extract_first(),
                'scale': tr.xpath('td[5]/text()').extract_first(),
                'rate': tr.xpath('td[6]/text()').extract_first(),
                'danwei': tr.xpath('td[7]/text()').extract_first(),
                'price': tr.xpath('td[8]/text()').extract_first(),
                'quality': tr.xpath('td[9]/text()').extract_first(),
                'pro_com': tr.xpath('td[10]/text()').extract_first(),
                'tou_com': tr.xpath('td[11]/text()').extract_first(),
                'province': tr.xpath('td[12]/text()').extract_first(),
                'date': tr.xpath('td[13]/text()').extract_first(),
                'beizhu': tr.xpath('td[14]/text()').extract_first(),
                'file': tr.xpath('td[15]/a/text()').extract_first(),
                'file_link': tr.xpath('td[15]/a/@href').extract_first(),
                'product': tr.xpath('td[16]/a/@href').extract_first(),
                'url': response.url
            }
            print(response.url)
            for i in range(1, page + 1):
                # url = self.start_urls[0].format(self.yname, self.zb_shengchanqiye, self.first, i)
                url = re.subn('p=\d+', 'p='+str(i), response.url)[0]
                # print(url)
                yield scrapy.Request(url, callback=self.parse)
        # except:
        #     print("==============maybe there is no result=============")
        #     print(response.url)
        #     self.log('may be no result')
        #     self.webdriver.get(response.url)
            # selector = Selector(text=self.webdriver.page_source)
            # next_page = selector.xpath('//div[@class="tr offset-top pagination"]/a/@href').extract()
            # next_page_num = next_page[len(next_page) - 1]
            # print(next_page_num)
            # os._exit(0)