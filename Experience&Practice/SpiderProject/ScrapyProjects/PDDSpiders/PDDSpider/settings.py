
BOT_NAME = 'pdd'

SPIDER_MODULES = ['PDDSpider.spiders']
NEWSPIDER_MODULE = 'PDDSpider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/7534.48.3'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
COOKIES_ENABLED = False

ITEM_PIPELINES = {'PDDSpider.pipelines.pddpipeline.PddspiderPipeline':0}

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "pdd"

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    "PDDSpider.middlewares.useragent.RandomUserAgentMiddleware": 500,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
    "PDDSpider.middlewares.proxy.ProxyMiddleware": 750,
}

TELNETCONSOLE_ENABLED = 0
REFERER_ENABLED = False
REDIRECT_ENABLED = False
RETRY_ENABLED = True  # not retry
RETRY_TIMES = 66  # initial response + 2 retries = 3 requests
RETRY_HTTP_CODES = [500, 501, 502, 503, 504, 408, 404, 403, 400, 405, 407, 429, 803, 301, 302, 303, 304, 307, 401, 413, 419, 408, 404, 403, 405, 407, 429]

SCHEDULER = 'PDDSpider.scrapy_redis.scheduler.Scheduler'
SCHEDULER_PERSIST = False
SCHEDULER_QUEUE_CLASS = 'PDDSpider.scrapy_redis.queue.SpiderQueue'

DUPEFILTER_CLASS = 'PDDSpider.scrapy_redis.dupefilter.RFPDupeFilter'

REDIE_URL = None
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

LOG_LEVEL = 'INFO'