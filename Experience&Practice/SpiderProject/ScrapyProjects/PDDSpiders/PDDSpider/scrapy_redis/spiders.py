from scrapy import Spider, signals
from scrapy.exceptions import DontCloseSpider

import sys
import os
from os.path import dirname

abs_path = dirname(dirname(os.path.abspath(__file__)))
abs_parent_path = dirname(abs_path)
sys.path.append(abs_path)
sys.path.append(abs_parent_path)

from PDDSpider.scrapy_redis import connection


class RedisMixin(object):
    """Mixin class to implement reading urls from a redis queue."""
    redis_key = None  # use default '<spider>:start_urls'

    def setup_redis(self):
        """Setup redis connection and idle signal.

        This should be called after the spider has set its crawler object.
        """
        self.redis_batch_size = 16
        if not self.redis_key:
            self.redis_key = '%s:start_urls' % self.name

        self.server = connection.from_settings(self.crawler.settings)
        # idle signal is called when the spider has no requests left,
        # that's when we will schedule new requests from redis queue
        self.crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)
        self.logger.info("Reading URLs from redis list '%s'" % self.redis_key)

    def next_request(self):
        """Returns a request to be scheduled or none."""
        found = 0
        while found < self.redis_batch_size:
            url = self.server.lpop(self.redis_key)
            if not url:
                break
            new_url = self.make_requests_from_url(url)
            yield new_url
            found += 1
        if found:
            self.logger.info('Read %s requests from "%s"', found, self.name)

    def schedule_next_request(self):
        """Schedules a request if available"""
        for req in self.next_request():
            self.crawler.engine.crawl(req, spider=self)

    def spider_idle(self):
        """Schedules a request if available, otherwise waits."""
        self.schedule_next_request()
        raise DontCloseSpider


class RedisSpider(RedisMixin, Spider):
    """Spider that reads urls from redis queue when idle."""

    def _set_crawler(self, crawler):
        super(RedisSpider, self)._set_crawler(crawler)
        self.setup_redis()
