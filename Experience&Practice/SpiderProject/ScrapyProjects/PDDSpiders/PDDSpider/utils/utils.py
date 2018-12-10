import redis

'''
    return: new item
'''


def generate_new_item(item: dict, key: str) -> dict:
    new_item = dict()
    new_item.update(item)
    new_item.update({'table_name': key})
    return new_item


REDIS_URI = "redis://127.0.0.1:6379/0"

'''
    return redis_object
'''


def generate_redis_conn() -> redis.StrictRedis:
    rcu = redis.StrictRedis().from_url(REDIS_URI)
    return rcu
