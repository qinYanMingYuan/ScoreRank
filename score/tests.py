from django.test import TestCase
from utils.redis_pool import POOL
import redis
from collections import OrderedDict
# Create your tests here.
import json
dict = {
    'name': '天哥',
    'fenshu': 23,
}
# value = json.dumps(dict)
conn = redis.Redis(connection_pool=POOL)
# conn.zadd('hehe', 'xiaohu', 12)
# conn.zadd('hehe', 'dahu', 13)
# conn.zincrby('hehe', 'dahu', 15)
# conn.zincrby('hehe', 'xiaohei', 15)
# conn.zincrby('hehe', value, 18)
# print(conn.zrevrange('hehe', 0, 3, True))
# print(type(json.loads(a)))
# print(conn.zcard('hehe'))
print(conn.zrevrank('hehe', 'xiaohu'))

# dic = OrderedDict()
# dic['name'] = 'hehe'
# print(dic['name'])
# print(int(-10))
