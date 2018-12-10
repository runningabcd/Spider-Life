import pymongo

from scrapy.conf import settings


class PddspiderPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.mall_rec_collection = db['mall_rec_list']
        self.goods_info_collection = db['goods_info']
        self.goods_rank_collection = db['goods_rank']

    def process_item(self, item, spider):
        if item['table_name'] == 'goods_info':
            try:
                item['_id'] = item['goods']['goods_id']
                self.goods_info_collection.insert(item)
            except Exception as e:
                spider.logger.error(str(e))
        elif item['table_name'] == 'mall_rec_list':
            try:
                item['_id'] = item['goods_id']
                self.mall_rec_collection.insert(item)
            except Exception as e:
                spider.logger.error(str(e))
        else:
            try:
                item['_id'] = item['goodsId']
                self.goods_rank_collection.insert(item)
            except Exception as e:
                if "'NoneType' object is not subscriptable" in str(e):
                    spider.logger.error(item)
                spider.logger.error(str(e))
        return None
