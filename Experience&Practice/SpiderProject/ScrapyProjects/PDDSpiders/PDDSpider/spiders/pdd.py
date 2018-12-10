from scrapy.http import Request, FormRequest

import ujson
import time
from urllib.parse import quote_plus

from PDDSpider.utils.utils import generate_new_item, generate_redis_conn
from PDDSpider.scrapy_redis.spiders import RedisSpider
from PDDSpider.scrapy_redis.queue import SpiderQueue
from PDDSpider.configs.pddconfig import config, cate_url, similar_url, detail_url, rank_url


class PddDetailSpider(RedisSpider):
    name = 'pdd_detail'
    allowed_domains = ['pinduoduo.com', 'yangkeduo.com']
    start_urls = []
    redis_key = '{}_queue'.format(name)

    def parse(self, response):
        result = ujson.loads(response.body.decode())
        yield generate_new_item(result, 'goods_info')


class PddListSpider(RedisSpider):
    name = 'pdd_list'
    allowed_domains = ['pinduoduo.com', 'yangkeduo.com']
    start_urls = ['https://mobile.yangkeduo.com/duo_cms_mall.html']
    redis_key = '{}_queue'.format(name)
    rcu = generate_redis_conn()
    detail_queue = SpiderQueue(rcu, PddDetailSpider(), 'pdd_detail_queue')

    def parse(self, response):
        '''
        :param response:
        :return: cate request
        '''
        '''
            post optid crawl goods rank list info
        '''
        # for cate in config:
        #     post_data = {"optId": str(cate.get('opt_id')), "pageNum": '0', "pageSize": '10'}
        #     yield FormRequest(cate_url, formdata=post_data, callback=self.parse_list,
        #                       meta={'opt_id': post_data.get('optId'), 'page_no': 0})
        #     for cate_child in cate.get('children'):
        #         post_data = {"optId": str(cate_child.get('opt_id')), "pageNum": '0', "pageSize": '10'}
        #         yield FormRequest(cate_url, formdata=post_data, callback=self.parse_list,
        #                           meta={'opt_id': post_data.get('optId'), 'page_no': 0})
        '''
           get optname crawl goods rank list info 
        '''
        for cate in config:
            opt_name = quote_plus(cate.get('opt_name'))
            yield Request(url=rank_url.format(opt_name, 0), callback=self.parse_list,
                          meta={'opt_name': opt_name, 'page_no': 0})
            for cate_child in cate.get('children'):
                opt_name = quote_plus(cate_child.get('opt_name'))
                yield Request(url=rank_url.format(opt_name, 0), callback=self.parse_list,
                              meta={'opt_name': opt_name, 'page_no': 0})

    def parse_list(self, response):
        '''
        :param response:
        :return: goods rank info item or similar request or cate request
        '''
        body = response.body.decode()
        result = ujson.loads(body)
        if 'SEARCH_ES_NULL' in body or 'SEARCH_NUM_LIMITED' in body:
            return
        try:
            goods_list = result['result']['goodsList']
        except Exception as e:
            self.logger.error(f'Request {response.url} error {str(e)}')
            new_req = response.request.copy()
            new_req.dont_filter = True
            yield new_req
            return
        for goods in goods_list:
            if not goods:
                continue
            yield generate_new_item(goods, 'goods_rank')
            goods_id = goods['goodsId']
            if not goods_id:
                continue
            # yield Request(url=similar_url.format(goods_id), callback=self.parse_similar)
            payload = {"address_list": [], "goods_id": str(goods_id), "page_from": "35", "page_version": "1",
                       "client_time": str(int(time.time() * 1000))}
            self.detail_queue.push(FormRequest(url=detail_url, formdata=payload))
        page_no = response.meta['page_no']
        if page_no:
            return
        # opt_id = response.meta['opt_id']
        # for x in range(1, 1000):
        #     post_data = {"optId": str(opt_id), "pageNum": str(x), "pageSize": '10'}
        #     yield FormRequest(cate_url, formdata=post_data, callback=self.parse_list,
        #                       meta={'opt_id': post_data.get('optId'), 'page_no': x})
        opt_name = response.meta['opt_name']
        total = result['result']['hitCount']
        page_no = (total // 20) + 1 if total % 20 else total // 20
        for x in range(1, page_no):
            yield Request(url=rank_url.format(opt_name, x), callback=self.parse_list,
                          meta={'opt_name': opt_name, 'page_no': x})

    def parse_similar(self, response):
        '''
        :param response: similar goods response
        :return: goods item or goods request or similar goods request
        '''
        result = ujson.loads(response.body.decode())
        info_lists = result.get('mall_rec_list', []) + result.get('list', [])
        for mall_rec in info_lists:
            yield generate_new_item(mall_rec, 'mall_rec_list')
            goods_id = mall_rec.get('goods_id')
            if not goods_id:
                continue
            payload = {"address_list": [], "goods_id": str(goods_id), "page_from": "35", "page_version": "1",
                       "client_time": str(int(time.time() * 1000))}
            self.detail_queue.push(FormRequest(url=detail_url, formdata=payload))
            yield Request(url=similar_url.format(goods_id), callback=self.parse_similar)
